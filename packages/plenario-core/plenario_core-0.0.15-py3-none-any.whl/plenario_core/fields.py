import json
from datetime import datetime
from typing import List, Type, Union

import arrow
from arrow.parser import ParserError
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point, LineString, Polygon, \
    MultiPoint, MultiLineString, MultiPolygon, GEOSGeometry
from marshmallow import ValidationError, fields
from psycopg2.extras import DateTimeTZRange

from plenario_core.enums import DjangoEnum
from plenario_core.utils import field_parsing as fp


class SourceFieldsConfigField(fields.Field):
    """A field for working with ``ds_source_fields`` data.
    """

    def _deserialize(self, value: dict, *args, **kwargs) -> List[dict]:
        """Parses input JSON and converts it to a configuration object.

        :param value: the JSON input to be converted
        :return: a configuration object for data set source fields
        :raise ValidationError: when it is not a valid configuration mapping
        """
        if not isinstance(value, dict):
            raise ValidationError('Not a valid configuration.')

        src_fields, errors = fp.deserialize_source_fields(value)
        if errors:
            raise ValidationError(errors)
        return src_fields


class PointFieldsConfigField(fields.Field):
    """A field for working with ``ds_configured_point_fields`` data.
    """

    def _deserialize(self, value: List[dict], *args, **kwargs) -> List[dict]:
        """Parses input JSON and converts it to a configuration object.

        :param value: the JSON input to be converted
        :return: a configuration object for dynamically parseable data set
            point fields
        :raise ValidationError: when it is not a valid configuration mapping
        """
        if not isinstance(value, list):
            raise ValidationError('Not a valid configuration.')

        for element in value:
            if not isinstance(element, dict):
                raise ValidationError('Not a valid configuration.')

        pt_fields, errors = fp.deserialize_configured_point_fields(value)
        if errors:
            raise ValidationError(errors)
        return pt_fields


class DateFieldsConfigField(fields.Field):
    """A field for working with ``ds_configured_date_fields`` data.
    """

    def _deserialize(self, value: List[dict], *args, **kwargs) -> List[dict]:
        """Parses input JSON and converts it to a configuration object.

        :param value: the JSON input to be converted
        :return: a configuration object for dynamically parseable data set
            datetime fields
        :raise ValidationError: when it is not a valid configuration mapping
        """
        if not isinstance(value, list):
            raise ValidationError('Not a valid configuration.')

        for element in value:
            if not isinstance(element, dict):
                raise ValidationError('Not a valid configuration.')

        dt_fields, errors = fp.deserialize_configured_date_fields(value)
        if errors:
            raise ValidationError(errors)
        return dt_fields


class UserEmailField(fields.Field):
    """A field for working with user model relations.
    """

    def _deserialize(self, value: str, *args, **kwargs) -> 'User':
        """Converts an email address to a proper User object

        :param value: user's email address
        :return: the full User model associated with the email address
        :raise ValidationError: when a user cannot be found
        """
        User = get_user_model()
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise ValidationError('Could not find user.')
        return user

    def _serialize(self, value: 'User', *args, **kwargs) -> str:
        return value.email


class TimeRangeField(fields.Field):
    """A field for working with ``psycopg2.extras.DateTimeTZRange`` values.
    """

    def _deserialize(self, value: dict, *args, **kwargs) -> DateTimeTZRange:
        """Converts a time range mapping to a DateTimeTZRange.

        :param value: the mapping containing ISO 8601 timestamps
        :return: the created time range
        :raise ValidationError: when the mapping cannot be converted
        """
        if not isinstance(value, dict):
            raise ValidationError('Value must be a mapping.')

        if not all(key in value for key in ['lower', 'upper']):
            raise ValidationError(
                'Value must contain "lower" and "upper" definitions.')

        try:
            lower = arrow.get(value['lower']).datetime
        except ParserError:
            raise ValidationError(f'Could not parse {value["lower"]}.')

        try:
            upper = arrow.get(value['upper']).datetime
        except ParserError:
            raise ValidationError(f'Could not parse {value["upper"]}.')

        dt = DateTimeTZRange(lower=lower, upper=upper)
        return dt

    def _serialize(
            self, value: DateTimeTZRange,
            *args, **kwargs) -> Union[List[str], None]:
        """Converts a DateTimeTZRange to a JSON object

        :param value: the time range field to be converted to JSON
        :return: the JSON conversion of the time range
        """
        if value:
            return [
                value.lower.isoformat(),
                value.upper.isoformat()
            ]
        return None


class DateTimeTZField(fields.Field):
    """A field for *properly* working with non-naive datetime objects.
    """

    def _serialize(self, value: datetime, *args, **kwargs) -> Union[str, None]:
        """Coverts a datetime object to a proper ISO 8601 timestamp.

        :param value: the datetime field to be converted to JSON
        :return: the ISO 8601 representation of the datetime value
        """
        if value:
            return value.isoformat()
        return None


class GeometryField(fields.Field):
    """A base class for geometric objects.
    """

    def _serialize(
            self, value: GEOSGeometry, *args, **kwargs) -> Union[dict, None]:
        """Converts a geometric object to GeoJSON.

        :param value: the object to be dumped to GeoJSON
        :return: the GeoJSON representation of the geometric object
        """
        if value:
            return json.loads(value.geojson)
        return None

    @staticmethod
    def _validate_shape(value: dict):
        """Ensures a given value can be parsed into a geometric object.
        """
        if not isinstance(value, dict):
            raise ValidationError('Not a valid GeoJSON object.')
        if not all(key in value for key in ['type', 'coordinates']):
            raise ValidationError('Not a valid GeoJSON object.')


class PointField(GeometryField):
    """A field for working with ``django.contrib.gis.geos.Point`` objects.
    """

    def _deserialize(self, value: dict, *args, **kwargs) -> Union[Point, None]:
        """Converts GeoJSON to a Point object.

        :param value: the GeoJSON to be converted
        :return: the Point object parsed from the GeoJSON
        :raise ValidationError: when the input value cannot be converted
        """
        self._validate_shape(value=value)
        if not value['type'].lower() == 'point':
            raise ValidationError('Not a valid Point object.')

        return Point(value['coordinates'])


class LineField(GeometryField):
    """A field for working with ``django.contrib.gis.geos.LineString`` objects.
    """

    def _deserialize(
            self, value: dict, *args, **kwargs) -> Union[LineString, None]:
        """Converts GeoJSON to a LineString object.

        :param value: the GeoJSON to be converted
        :return: the LineString object parsed from the GeoJSON
        :raise ValidationError: when the input value cannot be converted
        """
        self._validate_shape(value=value)
        if not value['type'].lower() == 'linestring':
            raise ValidationError('Not a valid Line object.')

        return LineString(value['coordinates'])


class PolygonField(GeometryField):
    """A field for working with ``django.contrib.gis.geos.Polygon`` objects.
    """

    def _deserialize(
            self, value: dict, *args, **kwargs) -> Union[Polygon, None]:
        """Converts GeoJSON to a Polygon object.

        :param value: the GeoJSON to be converted
        :return: the Polygon object parsed from the GeoJSON
        :raise ValidationError: when the input value cannot be converted
        """
        self._validate_shape(value=value)
        if not value['type'].lower() == 'polygon':
            raise ValidationError('Not a valid Polygon object.')

        return Polygon(value['coordinates'][0])


class MultiPointField(GeometryField):
    """A field for working with ``django.contrib.gis.geos.MultiPoint`` objects.
    """

    def _deserialize(
            self, value: dict, *args, **kwargs) -> Union[MultiPoint, None]:
        """Converts GeoJSON to a MultiPoint object.

        :param value: the GeoJSON to be converted
        :return: the MultiPoint object parsed from the GeoJSON
        :raise ValidationError: when the input value cannot be converted
        """
        self._validate_shape(value=value)
        if not value['type'].lower() == 'multipoint':
            raise ValidationError('Not a valid MultiPoint object.')

        points = []
        for pt in value['coordinates']:
            points.append(Point(pt))

        return MultiPoint(points)


class MultiLineField(GeometryField):
    """A field for working with ``django.contrib.gis.geos.MultiLineString``.
    """

    def _deserialize(
            self, value: dict, *args, **kwargs) -> Union[MultiLineString, None]:
        """Converts GeoJSON to a MultiLineString object.

        :param value: the GeoJSON to be converted
        :return: the MultiLineString object parsed from the GeoJSON
        :raise ValidationError: when the input value cannot be converted
        """
        self._validate_shape(value=value)
        if not value['type'].lower() == 'multilinestring':
            raise ValidationError('Not a valid Line object.')

        lines = []
        for ln in value['coordinates']:
            lines.append(LineString(ln))

        return MultiLineString(lines)


class MultiPolygonField(GeometryField):
    """A field for working with ``django.contrib.gis.geos.MultiPolygon``.
    """

    def _deserialize(
            self, value: dict, *args, **kwargs) -> Union[MultiPolygon, None]:
        """Converts GeoJSON to a MultiPolygon object.

        :param value: the GeoJSON to be converted
        :return: the MultiPolygon object parsed from the GeoJSON
        :raise ValidationError: when the input value cannot be converted
        """
        self._validate_shape(value=value)
        if not value['type'].lower() == 'multipolygon':
            raise ValidationError('Not a valid MultiPolygon object.')

        polygons = []
        for poly in value['coordinates']:
            polygons.append(Polygon(poly[0]))

        return MultiPolygon(polygons)


class EnumField(fields.Field):
    """A field for working with fields bound to an enum.
    """

    def __init__(self, enum_class: Type[DjangoEnum], *args, **kwargs) -> None:
        """Instantiates a new EnumField.

        :param enum_class: the type of enum to parse inputs to
        """
        super().__init__(*args, **kwargs)
        self.enum_class = enum_class

    def _deserialize(self, value: str, *args, **kwargs) -> str:
        """Converts a value to an enumeration.

        :param value: the value to look up in the configured enum
        :return: the enumeration value
        :raise ValidationError: when the value cannot be found in the enum
        """
        if self.enum_class.has_value(value):
            return value
        raise ValidationError(f'"{value}" is not a valid value.')


class DatasetExportField(fields.Field):
    default_error_messages = {
        'invalid': 'Not a valid dataset export mapping.'
    }

    def _deserialize(self, value: dict, *args, **kwargs) -> dict:
        if not isinstance(value, dict):
            self.fail('invalid')

        _required_keys = [
            'type', 'pk', 'filter_point_field', 'filter_date_field']
        _optional_keys = {
             'fields': fields.List(fields.Str()),
        }

        if not all(key in value for key in _required_keys):
            self.fail('invalid')

        result = {}
        for key in _required_keys:
            result[key] = value[key]

        for key, parser in _optional_keys.items():
            opt_value = value.get(key)
            if opt_value:
                deserialized, errors = parser.deserialize(opt_value)
                if errors:
                    self.fail('invalid')
                opt_value = deserialized
            result[key] = opt_value

        return result
