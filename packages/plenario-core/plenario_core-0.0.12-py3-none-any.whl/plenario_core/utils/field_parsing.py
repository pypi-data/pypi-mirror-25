from copy import copy
from typing import Dict, List, Set, Tuple, Type

from marshmallow import fields


_basic_ftypes: Set[str] = {
    'text',
    'integer',
    'decimal',
    'boolean',
}

_date_ftypes: Set[str] = {
    'date',
}

_geo_ftypes: Set[str] = {
    'point',
    'line',
    'polygon',
    'multi_point',
    'multi_line',
    'multi_polygon',
}

_field_types: Set[str] = _basic_ftypes | _date_ftypes | _geo_ftypes

_ftype_to_django: Dict[str, str] = {
    'text': 'TextField',
    'integer': 'IntegerField',
    'decimal': 'DecimalField',
    'boolean': 'NullBooleanField',
    'date': 'DateTimeField',
    'point': 'PointField',
    'line': 'LineStringField',
    'polygon': 'PolygonField',
    'multi_point': 'MultiPointField',
    'multi_line': 'MultiLineStringField',
    'multi_polygon': 'MultiPolygonField',
}

_django_date_ftypes: Set[str] = {
    'DateTimeField',
}

_django_geo_ftypes: Set[str] = {
    'PointField',
    'LineStringField',
    'PolygonField',
    'MultiPointField',
    'MultiLineStringField',
    'MultiPolygonField',
}

_django_to_serializer: Dict[str, Type[fields.Field]] = {
    'TextField': fields.Str,
    'IntegerField': fields.Int,
    'DecimalField': fields.Decimal,
    'NullBooleanField': fields.Bool,
    'DateTimeField': fields.DateTime,
    'PointField': fields.Str,
    'LineStringField': fields.Str,
    'PolygonField': fields.Str,
    'MultiPointField': fields.Str,
    'MultiLineStringField': fields.Str,
    'MultiPolygonField': fields.Str,
}

_default_django_kwargs = {'null': True, 'default': None}

_decimal_additional_kwargs = {'max_digits': 16, 'decimal_places': 10}


def deserialize_source_fields(
        user_definitions: dict) -> Tuple[List[dict], Dict[str, str]]:
    """Converts user input data to field mappings for a data set model.

    .. example::
    >>> from plenario_core.utils import field_parsing as fp
    >>> user_input = {
    ...     'name': 'text',
    ...     'location': 'point',
    ...     'date': 'date',
    ... }
    >>> src_fields, errors = fp.deserialize_source_fields(user_input)
    >>> assert errors == {}
    >>> assert src_fields == [
    ...     {
    ...         'name': 'name',
    ...         'class': 'TextField',
    ...         'kwargs': {'null': True, 'default': None},
    ...     },
    ...     {
    ...         'name': 'location',
    ...         'class': 'PointField',
    ...         'kwargs': {'null': True, 'default': None},
    ...     },
    ...     {
    ...         'name': 'date',
    ...         'class': 'DateTimeField',
    ...         'kwargs': {'null': True, 'default': None},
    ...     },
    ... ]

    :param user_definitions: a mapping of field keys and type values
    :return: the field configurations and any errors from parsing the input
    """

    field_defs: List[dict] = []
    errors: Dict[str, str] = {}

    for src_fname, ftype in user_definitions.items():
        # get the basics for creating the django field
        try:
            django_type = _ftype_to_django.get(ftype)
        except TypeError:  # NOQA
            django_type = None
        if not django_type:  # NOQA
            errors[src_fname] = f'{ftype} is not a valid type.'
            continue
        kwargs = copy(_default_django_kwargs)

        # splice in additional kwargs
        if ftype == 'decimal':
            kwargs.update(_decimal_additional_kwargs)

        # add the parsed definition
        field_defs.append({
            'name': src_fname,
            'class': django_type,
            'kwargs': kwargs,
        })

    return field_defs, errors


def deserialize_configured_point_fields(
        user_definitions: List[dict]) -> Tuple[List[dict], Dict[str, str]]:
    """Converts user input data to field mappings for parseable point fields.

    .. example::
    >>> from plenario_core.utils import field_parsing as fp
    >>> user_input = [
    ...     {
    ...         'latitude': 'lat',  # lat is a field name in the data set source
    ...         'longitude': 'long',  # so is long, they're both integers
    ...     },
    ...     {
    ...         'coordinates': 'coords'  # so is coords. it's a text field
    ...     }
    ... ]
    >>> pt_fields, errors = fp.deserialize_configured_point_fields(user_input)
    >>> assert errors == {}
    >>> assert pt_fields == [
    ...     {
    ...         'name': '_meta_point_0',
    ...         'class': 'PointField',
    ...         'kwargs': {'null': True, 'default': None},
    ...         'parsing_kwargs': {'latitude': 'lat', 'longitude': 'long'}
    ...     },
    ...     {
    ...         'name': '_meta_point_1',
    ...         'class': 'PointField',
    ...         'kwargs': {'null': True, 'default': None},
    ...         'parsing_kwargs': {'coordinates': 'coords'}
    ...     },
    ... ]

    :param user_definitions: a mapping of parsing name keys and field values
    :return: the field configurations and any errors from parsing the input
    """

    def _only_lat_long(mapping: dict):
        return set(mapping.keys()) == {'latitude', 'longitude'}

    def _only_coords(mapping: dict):
        return set(mapping.keys()) == {'coordinates'}

    pt_fields: List[dict] = []
    errors: Dict[str, str] = {}

    for idx, user_def in enumerate(user_definitions):
        if not _only_lat_long(user_def) and not _only_coords(user_def):
            errors[f'{idx}'] = 'You must specify either a "coordinate" field ' \
                               'of a set of "latitude" and "longitude" fields.'
            continue

        name = f'_meta_point_{idx}'
        kwargs = copy(_default_django_kwargs)

        pt_fields.append({
            'name': name,
            'class': 'PointField',
            'kwargs': kwargs,
            'parsing_kwargs': user_def,
        })

    return pt_fields, errors


def deserialize_configured_date_fields(
        user_definitions: List[dict]) -> Tuple[List[dict], Dict[str, str]]:
    """Converts user input data to field mappings for parseable date fields.

    .. example::
    >>> from plenario_core.utils import field_parsing as fp
    >>> user_input = [
    ...     {
    ...         'year': 'year',  # year is a field in source. it's an integer
    ...         'month': 'month',  # so is month
    ...         'day': 'day',  # so is day
    ...     }
    ... ]
    >>> dt_fields, errors = fp.deserialize_configured_date_fields(user_input)
    >>> assert errors == {}
    >>> assert dt_fields == [
    ...     {
    ...         'name': '_meta_date_0',
    ...         'class': 'DateTimeField',
    ...         'kwargs': {'null': True, 'default': None},
    ...         'parsing_kwargs': {
    ...             'year': 'year',
    ...             'month': 'month',
    ...             'day': 'day',
    ...             'hour': None,
    ...             'minute': None,
    ...             'second': None,
    ...         }
    ...     }
    ... ]

    :param user_definitions: a mapping of parsing name keys and field values
    :return: the field configurations and any errors from parsing the input
    """

    date_fields: List[dict] = []
    errors: Dict[str, str] = {}

    for idx, user_def in enumerate(user_definitions):
        year = user_def.get('year')
        if not year:
            errors[f'{idx}'] = 'You must specify at least a "year" value.'
            continue

        month = user_def.get('month')
        day = user_def.get('day')
        hour = user_def.get('hour')
        minute = user_def.get('minute')
        second = user_def.get('second')

        name = f'_meta_date_{idx}'
        kwargs = copy(_default_django_kwargs)

        date_fields.append({
            'name': name,
            'class': 'DateTimeField',
            'kwargs': kwargs,
            'parsing_kwargs': {
                'year': year,
                'month': month,
                'day': day,
                'hour': hour,
                'minute': minute,
                'second': second,
            }
        })

    return date_fields, errors


def add_srid_to_geo_fields(ds_fields: List[dict], srid: int) -> None:
    """Updates a field mapping's kwargs to include an SRID.

    :param ds_fields: the field mappings to update
    :param srid: the SRID to apply
    """
    for mapping in ds_fields:
        if mapping['class'] in _django_geo_ftypes:
            mapping['kwargs']['srid'] = srid
