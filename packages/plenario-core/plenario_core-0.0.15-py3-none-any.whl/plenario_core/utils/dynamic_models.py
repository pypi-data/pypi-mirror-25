from typing import Dict, List, Type

from django.contrib.gis.db import models as gis_models
from django.db import connection, models as dj_models
from django.db.models import Field, Model


def resolve_field(class_name: str, kwargs: dict) -> Field:
    """Converts a field configuration to a model field.

    .. example::
    >>> from django.db.models import TextField
    >>> from plenario_core.utils import dynamic_models as dm
    >>> field_config = {
    ...     'name': 'name',
    ...     'class': 'TextField',
    ...     'kwargs': {'null': True, 'default': None}
    ... }
    >>> field = dm.resolve_field(field_config['class'], field_config['kwargs'])
    >>> assert isinstance(field, TextField)
    >>> assert field.null is True
    >>> assert field.default is None

    :param class_name: the name of the model field class
    :param kwargs: kwargs to pass to init
    :return: the instantiated model field
    """
    try:
        klass = getattr(dj_models, class_name)
    except AttributeError:
        klass = getattr(gis_models, class_name)
    return klass(**kwargs)


def generate_model(
        model_name: str,
        table_name: str,
        fields: Dict[str, Field],
        dj_app_label: str='dynamic') -> Type[Model]:
    """Dynamically creates a model for a data set.

    :param model_name: the name of the model object
    :param table_name: the database table name to work with
    :param fields: the field configurations for the model
    :param dj_app_label: the django app label for the model
    :return: the configured model for the data set
    """
    class Meta:
        app_label = dj_app_label
        db_table = table_name

    attrs = {
        '__module__': dj_app_label,
        'Meta': Meta,
    }
    attrs.update(fields)

    model = type(model_name, (Model,), attrs)
    return model


def create_table(model: Type[Model]) -> None:
    """Creates a database table for a given data set model.
    """
    with connection.schema_editor() as se:
        se.create_model(model)


def drop_table(model: Type[Model]) -> None:
    """Drops a database table for a given data set model.
    """
    with connection.schema_editor() as se:
        se.delete_model(model)


def get_subclasses(model: Type[Model]) -> List[Type[Model]]:
    """Gets a list of all concrete models the inherit from the given model.

    :param model: the model class to find all descendants
    :return: a list of concrete model descendants
    """
    subclasses = []
    todo = [model]
    while todo:
        parent = todo.pop()
        for child in parent.__subclasses__():
            todo.append(child)
            if child not in subclasses and not child._meta.abstract:
                subclasses.append(child)
    return subclasses
