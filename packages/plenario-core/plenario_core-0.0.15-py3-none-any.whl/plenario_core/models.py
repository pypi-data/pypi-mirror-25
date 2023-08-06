from datetime import datetime
from typing import List, Optional, Type, Union

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import ProgrammingError, models
from django.db.models import Model
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from plenario_core import mixins, signals
from plenario_core.utils import dynamic_models
from plenario_core.validators import starts_with_letter


class MetaBase(models.Model):
    """An abstract base class for all meta data models in the system.
    """

    class Meta:
        abstract = True

    name: str = models.TextField(
        unique=True,
        help_text=_('The name of the data set.'))
    contributor: 'User' = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        help_text=_('The owner of the data set.'))
    slug: str = models.SlugField(
        unique=True,
        blank=True,
        editable=False,
        help_text=_('String identifier - used in URLs.'))

    description: Optional[Union[str, None]] = models.TextField(
        null=True,
        default=None,
        blank=True,
        help_text=_('A description of the data set.'))
    attribution: Optional[Union[str, None]] = models.TextField(
        null=True,
        default=None,
        blank=True,
        help_text=_('Where the data set was sourced from.'))
    date_created: datetime = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        help_text=_('The date the meta data was created.'))
    date_updated: datetime = models.DateTimeField(
        auto_now=True,
        blank=True,
        help_text=_('The date the meta data was last updated.'))

    ds_first_run_date: Optional[Union[datetime, None]] = models.DateTimeField(
        null=True,
        default=None,
        help_text=_('The date the data set was first processed.'))
    ds_last_run_date: Optional[Union[datetime, None]] = models.DateTimeField(
        null=True,
        default=None,
        help_text=_('The date the data set was last processed.'))
    ds_source_fields: Optional[List[dict]] = JSONField(
        default=[],
        blank=True,
        help_text=_('Mapping of source fields to Django fields.'))

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        """On first save, validates the name and creates the slug.
        """
        send_registered_signal = False

        if not self.pk:
            # validate the name
            starts_with_letter(self.name)
            # create the slug
            self.slug = slugify(self.name, allow_unicode=True)
            # flip signal bit
            send_registered_signal = True

        super().save(*args, **kwargs)

        if send_registered_signal:
            signals.data_set_registered.send(
                sender=self.__class__, meta_model=self)

    def delete(self, *args, **kwargs):
        """Deletes data set table if it exists before deleting itself.
        """
        try:
            ds_model = self.get_ds_model()
            dynamic_models.drop_table(ds_model)
        except ProgrammingError:
            pass
        super().delete(*args, **kwargs)

    def get_ds_table_name(self) -> str:
        """Builds the data set table name from the slug.

        :return: the name of the data set table
        """
        name = self.slug.replace('-', '_')
        name = f'{name}__{self.__class__.__name__.lower()}'
        return name

    def get_ds_model_name(self) -> str:
        """Builds the model name for the data set from the slug.

        :return: the name of the data set model
        """
        name = self.slug.replace('-', ' ').title().replace(' ', '')
        name = f'{name}{self.__class__.__name__}'
        return name

    def get_ds_fields(self) -> List[dict]:
        """Gets the full list of all fields for the data set model.

        .. note:: at a minimum, this needs to be implemented by inheritors

        :return: the fields of the data set model
        """
        raise NotImplementedError

    def get_ds_model(self) -> Type[Model]:
        """Dynamically builds a Django model for the data set.

        :return: a Django model for the data set
        """
        ds_fields = self.get_ds_fields()
        ds_model_name = self.get_ds_model_name()
        ds_table_name = self.get_ds_table_name()

        fields = {
            f['name']: dynamic_models.resolve_field(f['class'], f['kwargs'])
            for f in ds_fields
        }
        model = dynamic_models.generate_model(
            model_name=ds_model_name,
            table_name=ds_table_name,
            fields=fields
        )
        return model

    @models.permalink
    def get_absolute_url(self) -> str:
        """Gets a URI for the model.

        .. note:: this needs to be implemented by concrete models
        .. note:: this is used by the default base serializer

        :return: the URI of the model
        """
        raise NotImplementedError


class ShapeMetaBase(mixins.GeoMixin, mixins.EtlDataMixin, MetaBase):
    """An abstract base class for shapefile data.
    """

    class Meta:
        abstract = True
        verbose_name = 'Shapefile Data Set'

    def get_ds_fields(self) -> List[dict]:
        """Gets the full list of all fields for the data set model.

        :return: the fields of the data set model
        """
        return [*self.ds_source_fields, *self.ds_configured_point_fields]


class EtlEventMetaBase(
        mixins.GeoMixin, mixins.TimeMixin, mixins.EtlDataMixin, MetaBase):
    """An abstract base class for event data consumed via an ETL process.
    """

    class Meta:
        abstract = True
        verbose_name = 'ETL Event Data Set'

    def get_ds_fields(self) -> List[dict]:
        """Gets the full list of all fields for the data set model.

        :return: the fields of the data set model
        """
        return [
            *self.ds_source_fields,
            *self.ds_configured_point_fields,
            *self.ds_configured_date_fields]


class StreamingEventMetaBase(
        mixins.GeoMixin, mixins.TimeMixin, mixins.StreamingDataMixin, MetaBase):
    """An abstract base class for event data consumed via a streaming process.
    """

    class Meta:
        abstract = True
        verbose_name = 'Stream Event Data Set'

    def get_ds_fields(self) -> List[dict]:
        """Gets the full list of all fields for the data set model.

        :return: the fields of the data set model
        """
        return [
            *self.ds_source_fields,
            *self.ds_configured_point_fields,
            *self.ds_configured_date_fields]


class EtlSensorNetEventMetaBase(mixins.SensorNetMixin, EtlEventMetaBase):
    """An abstract base class for sensor net event data consumed via ETL.
    """

    class Meta:
        abstract = True
        verbose_name = 'ETL SensorNet Event Data Set'


class StreamingSensorNetEventMetaBase(
        mixins.SensorNetMixin, StreamingEventMetaBase):
    """An abstract base class for sensor net event data consumed via streams.
    """

    class Meta:
        abstract = True
        verbose_name = 'Stream SensorNet Event Data Set'
