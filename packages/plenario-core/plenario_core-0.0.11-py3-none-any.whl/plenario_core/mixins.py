import logging
import secrets
from datetime import datetime
from random import choice
from typing import List, Optional, Union

import arrow
from django.contrib.gis.db.models import PolygonField
from django.contrib.gis.geos import Polygon
from django.contrib.postgres.fields import DateTimeRangeField, JSONField
from django.db import models
from django.db.models import Manager
from django.utils.translation import ugettext_lazy as _
from django_fsm import ConcurrentTransitionMixin, FSMField, transition
from psycopg2.extras import DateTimeTZRange

from plenario_core import defaults, managers, signals
from plenario_core.enums import EtlState, StreamState, RefreshRate
from plenario_core.utils import dynamic_models
from plenario_core.utils.postgres import date_triggers, geo_triggers

logger = logging.getLogger(__name__)

_hour_choices = range(0, 23)
_minute_choices = range(0, 59)


class EtlDataMixin(ConcurrentTransitionMixin, models.Model):
    """An abstract base class providing fields for ETL consumption.
    """

    class Meta:
        abstract = True

    # required fields
    source_url: str = models.URLField(
        unique=True,
        help_text=_('The source URL of the public data set.'))

    # optional refresh information
    refresh_rate: Optional[RefreshRate] = models.TextField(
        default=RefreshRate.Never.value,
        choices=RefreshRate.as_choices(),
        blank=True,
        help_text=_('Time period for processing the data set.'))
    refresh_interval: Optional[int] = models.PositiveIntegerField(
        null=True,
        default=None,
        blank=True,
        help_text=_('Offset for the time period for processing the data set.'))
    refresh_starts_on: Optional[Union[datetime, None]] = models.DateTimeField(
        null=True,
        default=None,
        blank=True,
        help_text=_('A specific date to wait until before processing the data'))

    # automated refresh dates
    last_refreshed: Union[datetime, None] = models.DateTimeField(
        null=True,
        default=None,
        blank=True,
        help_text=_('The date the data set was last processed.'))
    next_refresh: Union[datetime, None] = models.DateTimeField(
        null=True,
        default=None,
        blank=True,
        help_text=_('The next date the data set will be processed.'))

    # fsm lock
    state: EtlState = FSMField(
        default=EtlState.New.value,
        protected=True,
        help_text=_('Processing state of the data set.'))

    # custom managers
    objects: Manager = Manager()
    new_objects: Manager = managers.EtlNewManager()
    approved_objects: Manager = managers.EtlApprovedManager()
    ready_objects: Manager = managers.EtlReadyManager()
    locked_objects: Manager = managers.EtlLockedManager()
    erred_objects: Manager = managers.EtlErredManager()

    def compute_next_refresh(self) -> Union[datetime, None]:
        """Computes the next time the data is consumed via the ETL pipeline.

        :return: the date the next ingest process should run
        """
        # force string in case of enum
        self.refresh_rate = str(self.refresh_rate)

        # if this is not supposed to be refreshed, exit
        if self.refresh_rate == RefreshRate.Never.value:
            return None

        # if this was never refreshed, start now or on specified start date
        if not self.last_refreshed:
            if self.refresh_starts_on:
                return arrow.get(self.refresh_starts_on).datetime
            return arrow.utcnow().datetime

        # if this is a quick periodic refresh, use now + offset
        if self.refresh_rate == RefreshRate.Minutes.value:
            return arrow.get(self.last_refreshed).shift(
                minutes=self.refresh_interval)

        if self.refresh_rate == RefreshRate.Hours.value:
            return arrow.get(self.last_refreshed).shift(
                hours=self.refresh_interval)

        # if this is a typical refresh, shift
        last_run = arrow.get(self.last_refreshed.date())
        if self.refresh_rate == RefreshRate.Days.value:
            nr = last_run.shift(days=self.refresh_interval)
        elif self.refresh_rate == RefreshRate.Months.value:
            nr = last_run.shift(months=self.refresh_interval)
        elif self.refresh_rate == RefreshRate.Years.value:
            nr = last_run.shift(years=self.refresh_interval)
        else:
            logger.error(
                f'Tried to compute next refresh date for data set '
                f'"{self.name}" with refresh rate "{self.refresh_rate}".')
            raise ValueError(
                f'Could not compute refresh for rate "{self.refresh_rate}".')

        # randomize the time
        hours = choice(_hour_choices)
        minutes = choice(_minute_choices)
        nr = nr.shift(hours=hours, minutes=minutes)
        return nr.datetime

    @transition(
        field=state,
        source=EtlState.New.value,
        target=EtlState.Approved.value)
    def approve(self) -> None:
        """Sets the ``state`` to approved.
        """
        logger.info(f'Approving data set "{self.name}".')
        signals.data_set_approved.send(sender=self.__class__, meta_model=self)

    @transition(
        field=state,
        source=EtlState.Approved.value,
        target=EtlState.Ready.value,
        on_error=EtlState.Erred.value)
    def create_data_set_table(self) -> None:
        """Sets the ``state`` to ready after creating the data set table.
        """
        logger.info(f'Creating table for data set "{self.name}".')
        model = self.get_ds_model()
        dynamic_models.create_table(model=model)
        if isinstance(self, GeoMixin):
            geo_triggers.add_point_triggers(self)
        if isinstance(self, TimeMixin):
            date_triggers.add_date_triggers(self)
        signals.data_set_table_created.send(
            sender=self.__class__, meta_model=self)

    @transition(
        field=state,
        source=[EtlState.Ready.value, EtlState.Erred.value],
        target=EtlState.Approved.value,
        on_error=EtlState.Erred.value)
    def drop_data_set_table(self, reason: str) -> None:
        """Sets the ``state`` to approved after dropping the data set table.

        :param reason: a message to log about why the drop is happening
        """
        logger.info(
            f'Dropping table for data set "{self.name}" because: {reason}')
        model = self.get_ds_model()
        dynamic_models.drop_table(model=model)
        signals.data_set_table_dropped.send(
            sender=self.__class__, meta_model=self, reason=reason)

    @transition(
        field=state,
        source=EtlState.Ready.value,
        target=EtlState.Locked.value)
    def lock_data_set_table_before_swap(self) -> None:
        """Sets the ``state`` to locked while data set tables are transferred.
        """
        logger.info(f'Swapping data set table for "{self.name}".')

    @transition(
        field=state,
        source=EtlState.Locked.value,
        target=EtlState.Ready.value)
    def unlock_data_set_table_after_swap(self) -> None:
        """Sets the ``state`` to ready after the tables are transferred.
        """
        logger.info(f'Table swap complete for "{self.name}".')

    @transition(
        field=state,
        source='*',
        target=EtlState.Erred.value)
    def mark_erred(self, reason: str) -> None:
        """Sets the ``state`` to erred when an error is encountered.

        :param reason: a message to log about what went wrong
        """
        logger.error(f'Marking data set "{self.name}" as erred: {reason}')
        signals.data_set_erred.send(
            sender=self.__class__, meta_model=self, reason=reason)

    @transition(
        field=state,
        source=EtlState.Erred.value,
        target=EtlState.Ready.value)
    def mark_fixed(self, reason: str) -> None:
        """Sets the ``state`` to ready after an error is fixed.

        :param reason: a message to log about the fix
        """
        logger.info(f'Marking data set "{self.name}" as fixed: {reason}')
        signals.data_set_fixed.send(
            sender=self.__class__, meta_model=self, reason=reason)


class StreamingDataMixin(ConcurrentTransitionMixin, models.Model):
    """An abstract base class providing fields for streaming consumption.
    """

    class Meta:
        abstract = True

    # stream control fields
    _token: str = models.TextField(
        verbose_name='token',
        db_column='token',
        unique=True,
        blank=True,
        editable=False,
        help_text=_('ID and auth token for sending data to the system.'))
    is_relayed: Union[bool, None] = models.NullBooleanField(
        blank=True,
        help_text=_('Should the received data be relayed to the public?'))

    # fsm lock
    state: StreamState = FSMField(
        default=StreamState.New.value,
        protected=True,
        help_text=_('Processing state of the data set.'))

    objects: Manager = Manager()
    new_objects: Manager = managers.StreamNewManager()
    approved_objects: Manager = managers.StreamApprovedManager()
    ready_objects: Manager = managers.StreamReadyManager()
    erred_objects: Manager = managers.StreamErredManager()

    def save(self, *args, **kwargs):
        """Creates the token on first save.
        """
        if not self.pk:
            self._token = secrets.token_hex()
        super().save(*args, **kwargs)

    @property
    def token(self) -> str:
        return self._token

    @transition(
        field=state,
        source=EtlState.New.value,
        target=EtlState.Approved.value)
    def approve(self) -> None:
        """Sets the ``state`` to approved.
        """
        logger.info(f'Approving data set "{self.name}".')
        signals.data_set_approved.send(sender=self.__class__, meta_model=self)

    @transition(
        field=state,
        source=EtlState.Approved.value,
        target=EtlState.Ready.value,
        on_error=EtlState.Erred.value)
    def create_data_set_table(self) -> None:
        """Sets the ``state`` to ready after creating the data set table.
        """
        logger.info(f'Create table for data set "{self.name}".')
        model = self.get_ds_model()
        dynamic_models.create_table(model=model)
        if isinstance(self, GeoMixin):
            geo_triggers.add_point_triggers(self)
        if isinstance(self, TimeMixin):
            date_triggers.add_date_triggers(self)
        signals.data_set_table_created.send(
            sender=self.__class__, meta_model=self)

    @transition(
        field=state,
        source=[EtlState.Ready.value, EtlState.Erred.value],
        target=EtlState.Approved.value,
        on_error=EtlState.Erred.value)
    def drop_data_set_table(self, reason: str) -> None:
        """Sets the ``state`` to approved after dropping the data set table.

        :param reason: a message to log about why the drop is happening
        """
        logger.info(
            f'Dropping table for data set "{self.name}" because: {reason}')
        model = self.get_ds_model()
        dynamic_models.drop_table(model=model)
        signals.data_set_table_dropped.send(
            sender=self.__class__, meta_model=self)

    @transition(
        field=state,
        source='*',
        target=EtlState.Erred.value)
    def mark_erred(self, reason: str) -> None:
        """Sets the ``state`` to erred when an error is encountered.

        :param reason: a message to log about what went wrong
        """
        logger.error(f'Marking data set "{self.name}" as erred: {reason}')
        signals.data_set_erred.send(
            sender=self.__class__, meta_model=self, reason=reason)

    @transition(
        field=state,
        source=EtlState.Erred.value,
        target=EtlState.Ready.value)
    def mark_fixed(self, reason: str) -> None:
        """Sets the ``state`` to ready after an error is fixed.

        :param reason: a message to log about the fix
        """
        logger.info(f'Marking data set "{self.name}" as fixed: {reason}')
        signals.data_set_fixed.send(
            sender=self.__class__, meta_model=self, reason=reason)


class GeoMixin(models.Model):
    """An abstract base class that provides fields for data sets with geo info.
    """

    class Meta:
        abstract = True

    ds_srid: Optional[str] = models.TextField(
        default=defaults.SRID,
        blank=True,
        help_text=_('The SRID applied to geometry fields.'))
    ds_bbox: Union[Polygon, None] = PolygonField(
        null=True,
        default=None,
        blank=True,
        help_text=_('A bounding box surrounding the data set geometry fields.'))
    ds_configured_point_fields: List[dict] = JSONField(
        default=[],
        blank=True,
        help_text=_('User configured point fields composed of source fields.'))


class TimeMixin(models.Model):
    """An abstract base class that provides fields for data sets with time info.
    """

    class Meta:
        abstract = True

    ds_timezone: Optional[str] = models.TextField(
        default=defaults.TIMEZONE,
        blank=True,
        help_text=_('The timezone applied to date fields.'))
    ds_timerange: DateTimeTZRange = DateTimeRangeField(
        null=True,
        default=None,
        blank=True,
        help_text=_('A time range the encompasses the data set date fields.'))
    ds_configured_date_fields: List[dict] = JSONField(
        default=[],
        blank=True,
        help_text=_('User configured date fields composed of source fields.'))


class SensorNetMixin(models.Model):
    """An abstract base class that provides fields for data sets with net info.
    """

    class Meta:
        abstract = True

    nodes: Optional[List[dict]] = JSONField(
        default=[],
        blank=True,
        help_text=_('Mapping of node information.'))
