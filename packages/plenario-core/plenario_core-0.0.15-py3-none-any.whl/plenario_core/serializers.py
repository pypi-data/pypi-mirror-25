from plenario_core import schemas


class ShapeMetaBaseSerializer(
        schemas.GeoMixinSerializerSchema,
        schemas.EtlDataMixinSerializerSchema,
        schemas.MetaBaseSerializerSchema):
    """A default serializer implementation for shapefiles.
    """
    pass


class EtlEventMetaBaseSerializer(
        schemas.GeoMixinSerializerSchema,
        schemas.TimeMixinSerializerSchema,
        schemas.EtlDataMixinSerializerSchema,
        schemas.MetaBaseSerializerSchema):
    """A default serializer implementation for ETL Event data.
    """
    pass


class StreamingEventMetaBaseSerializer(
        schemas.GeoMixinSerializerSchema,
        schemas.TimeMixinSerializerSchema,
        schemas.StreamingDataMixinSerializerSchema,
        schemas.MetaBaseSerializerSchema):
    """A default serializer implementation for Streaming Event data.
    """
    pass


class EtlSensorNetEventMetaBaseSerializer(
        schemas.GeoMixinSerializerSchema,
        schemas.TimeMixinSerializerSchema,
        schemas.EtlDataMixinSerializerSchema,
        schemas.MetaBaseSerializerSchema,
        schemas.SensorNetMixinSerializerSchema):
    """A default serializer implementation for ETL Sensor Event data.
    """
    pass


class StreamingSensorNetEventMetaBaseSerializer(
        schemas.GeoMixinSerializerSchema,
        schemas.TimeMixinSerializerSchema,
        schemas.StreamingDataMixinSerializerSchema,
        schemas.MetaBaseSerializerSchema,
        schemas.SensorNetMixinSerializerSchema):
    """A default serializer implementation for Streaming Sensor Event data.
    """
    pass
