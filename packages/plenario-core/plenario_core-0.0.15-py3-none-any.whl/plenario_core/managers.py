from django.db import models
from django.db.models import QuerySet

from plenario_core.enums import EtlState, StreamState


class EtlNewManager(models.Manager):
    """A manager for working with *new* state data for ETL models.
    """

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        """Provides a default queryset with only *new* state models.
        """
        return super().get_queryset(*args, **kwargs).filter(
            state=EtlState.New.value)


class EtlApprovedManager(models.Manager):
    """A manager for working with *approved* state data for ETL models.
    """

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        """Provides a default queryset with only *approved* state models.
        """
        return super().get_queryset(*args, **kwargs).filter(
            state=EtlState.Approved.value)


class EtlLockedManager(models.Manager):
    """A manager for working with *locked* state data for ETL models.
    """

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        """Provides a default queryset with only *locked* state models.
        """
        return super().get_queryset(*args, **kwargs).filter(
            state=EtlState.Locked.value)


class EtlErredManager(models.Manager):
    """A manager for working with *erred* state data for ETL models.
    """

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        """Provides a default queryset with only *erred* state models.
        """
        return super().get_queryset(*args, **kwargs).filter(
            state=EtlState.Erred.value)


class EtlReadyManager(models.Manager):
    """A manager for working with *ready* state data for ETL models.
    """

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        """Provides a default queryset with only *ready* state models.
        """
        return super().get_queryset(*args, **kwargs).filter(
            state=EtlState.Ready.value)


class StreamNewManager(models.Manager):
    """A manager for working with *new* state data for streaming models.
    """

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        """Provides a default queryset with only *new* state models.
        """
        return super().get_queryset(*args, **kwargs).filter(
            state=StreamState.New.value)


class StreamApprovedManager(models.Manager):
    """A manager for working with *approved* state data for streaming models.
    """

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        """Provides a default queryset with only *approved* state models.
        """
        return super().get_queryset(*args, **kwargs).filter(
            state=StreamState.Approved.value)


class StreamErredManager(models.Manager):
    """A manager for working with *erred* state data for streaming models.
    """

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        """Provides a default queryset with only *erred* state models.
        """
        return super().get_queryset(*args, **kwargs).filter(
            state=StreamState.Erred.value)


class StreamReadyManager(models.Manager):
    """A manager for working with *ready* state data for streaming models.
    """

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        """Provides a default queryset with only *ready* state models.
        """
        return super().get_queryset(*args, **kwargs).filter(
            state=StreamState.Ready.value)
