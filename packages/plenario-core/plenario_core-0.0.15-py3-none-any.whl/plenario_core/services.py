import logging
from typing import List, Optional, Type, Union

from django.db.models import QuerySet
from marshmallow import Schema, ValidationError

from plenario_core import defaults
from plenario_core.models import MetaBase
from plenario_core.utils import field_parsing


logger = logging.getLogger(__name__)


def serialize_meta_model(
        instance: Union[MetaBase, QuerySet],
        serializer: Schema,
        many: Optional[bool]=False) -> Union[dict, List[dict]]:
    """Converts a model or queryset to JSON using a given serializer.

    :param instance: the model or queryset to convert
    :param serializer: the schema used to convert ``instance``
    :param many: is there more than one instance being converted?
    :return: the serialized value of ``instance``
    """
    serialized, errors = serializer.dump(instance, many=many)

    if errors:  # NOQA
        logger.error(
            f'Errors from serializing meta data "{instance.name}": {errors}')

    return serialized


def deserialize_to_meta_model(
        payload: dict,
        deserializer: Schema,
        model_class: Type[MetaBase],
        instance: Optional[MetaBase]=None,
        partial: Optional[bool]=False) -> MetaBase:
    """Converts a JSON object to a model instance.

    :param payload: the JSON to be converted
    :param deserializer: the schema used to convert ``payload``
    :param model_class: the model type to create from a valid payload
    :param instance: an existing model instance to update
    :param partial: is this only a partial update?
    :return: a new or updated model instance from the payload
    :raise ValidationError: when the payload does not satisfy the deserializer
    """
    deserialized, errors = deserializer.load(payload, partial=partial)

    if errors:
        raise ValidationError(errors)

    if 'ds_srid' in deserialized:
        srid = deserialized['ds_srid']
    else:
        srid = defaults.SRID

    if 'ds_source_fields' in deserialized:
        source_fields, errors = \
            field_parsing.deserialize_source_fields(
                deserialized['ds_source_fields'])
        if errors:
            raise ValidationError(errors)
        field_parsing.add_srid_to_geo_fields(source_fields, srid)
        deserialized['ds_source_fields'] = source_fields

    if 'ds_configured_point_fields' in deserialized:
        point_fields, errors = \
            field_parsing.deserialize_configured_point_fields(
                deserialized['ds_configured_point_fields'])
        if errors:
            raise ValidationError(errors)
        field_parsing.add_srid_to_geo_fields(point_fields, srid)
        deserialized['ds_configured_point_fields'] = point_fields

    if 'ds_configured_date_fields' in deserialized:
        date_fields, errors = \
            field_parsing.deserialize_configured_date_fields(
                deserialized['ds_configured_date_fields'])
        if errors:
            raise ValidationError(errors)
        deserialized['ds_configured_date_fields'] = date_fields

    if not instance:
        instance = model_class(**deserialized)
    else:
        for key, value in deserialized.items():
            setattr(instance, key, value)

    return instance
