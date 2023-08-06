from marshmallow import Schema, fields

from plenario_core import fields as pcfields
from plenario_core.enums import RefreshRate
from plenario_core.models import MetaBase


class MetaBaseSerializerSchema(Schema):
    """A schema for transforming basic MetaBase models to JSON.
    """

    name = fields.Str(required=True)
    contributor = pcfields.UserEmailField(required=True)
    description = fields.Str(allow_none=True)
    attribution = fields.Str(allow_none=True)
    date_created = pcfields.DateTimeTZField()
    date_updated = pcfields.DateTimeTZField()
    ds_first_run_date = pcfields.DateTimeTZField(allow_none=True)
    ds_last_run_date = pcfields.DateTimeTZField(allow_none=True)
    ds_source_fields = fields.List(fields.Dict(), allow_none=True)
    uri = fields.Method('get_uri')
    pk = fields.Int(required=True)
    type = fields.Method('get_type')

    def get_uri(self, obj: MetaBase) -> str:
        return obj.get_absolute_url()

    def get_type(self, obj: MetaBase) -> str:
        return obj.__class__.__name__


class EtlDataMixinSerializerSchema(Schema):
    """A schema for transforming ``EtlDataMixin`` fields to JSON.
    """

    source_url = fields.Url(allow_none=False)
    refresh_rate = fields.Str(required=True)
    refresh_interval = fields.Int(allow_none=True)
    refresh_starts_on = pcfields.DateTimeTZField(allow_none=True)
    last_refreshed = pcfields.DateTimeTZField(allow_none=True)
    next_refresh = pcfields.DateTimeTZField(allow_none=True)
    state = fields.Str(required=True)


class StreamingDataMixinSerializerSchema(Schema):
    """A schema for transforming ``StreamingDataMixin`` fields to JSON.
    """

    token = fields.Str(required=True)
    is_relayed = fields.Bool(required=True)
    state = fields.Str(required=True)


class GeoMixinSerializerSchema(Schema):
    """A schema for transforming ``GeoMixin`` fields to JSON.
    """

    ds_srid = fields.Str(required=True)
    ds_bbox = pcfields.PolygonField(allow_none=True)
    ds_configured_point_fields = fields.List(fields.Dict(), allow_none=True)


class TimeMixinSerializerSchema(Schema):
    """A schema for transforming ``TimeMixin`` fields to JSON.
    """

    ds_timezone = fields.Str(required=True)
    ds_timerange = pcfields.TimeRangeField(allow_none=True)
    ds_configured_date_fields = fields.List(fields.Dict(), allow_none=True)


class SensorNetMixinSerializerSchema(Schema):
    """A schema for transforming ``SensorNetMixin`` fields to JSON.
    """

    nodes = fields.List(fields.Dict(), allow_none=True)


class MetaBaseDeserializerSchema(Schema):
    """A schema for transforming JSON to ``MetaBase`` attributes.
    """

    name = fields.Str(required=True)
    contributor = pcfields.UserEmailField(required=True)
    description = fields.Str(allow_none=True)
    attribution = fields.Str(allow_none=True)
    ds_source_fields = fields.Dict(allow_none=True)


class EtlDataMixinDeserializerSchema(Schema):
    """A schema for transforming JSON to ``EtlDataMixin`` attributes.
    """

    source_url = fields.Url(required=True)
    refresh_rate = pcfields.EnumField(enum_class=RefreshRate, allow_none=True)
    refresh_interval = fields.Int(allow_none=True)
    refresh_starts_on = pcfields.DateTimeTZField(allow_none=True)


class StreamingDataMixinDeserializerSchema(Schema):
    """A schema for transforming JSON to ``StreamingDataMixin`` attributes.
    """

    is_relayed = fields.Bool(allow_none=True)


class SensorNetMixinDeserializerSchema(Schema):
    """A schema for transforming JSON to ``SensorNetMixin`` attributes.
    """

    nodes = fields.List(fields.Dict(), allow_none=True)


class GeoMixinDeserializerSchema(Schema):
    """A schema for transforming JSON to ``GeoMixin`` attributes.
    """

    ds_srid = fields.Str(allow_none=True)
    ds_configured_point_fields = fields.List(fields.Dict(), allow_none=True)


class TimeMixinDeserializerSchema(Schema):
    """A schema for transforming JSON to ``TimeMixin`` attributes.
    """

    ds_timezone = fields.Str(allow_none=True)
    ds_configured_date_fields = fields.List(fields.Dict(), allow_none=True)


class SearchSchema(Schema):
    """A schema for transforming JSON to fields used to perform searches.
    """

    ds_timerange = pcfields.TimeRangeField(required=True)
    ds_bbox = pcfields.PolygonField(required=True)


class ExportRequestSchema(Schema):
    data_sets = fields.List(
        pcfields.DatasetExportField(required=True),
        required=True)
    email_address = pcfields.UserEmailField(required=True)
    ds_timerange = pcfields.TimeRangeField(required=True)
    ds_bbox = pcfields.PolygonField(required=True)
