from plenario_core import schemas


class ShapeMetaBaseDeserializer(
        schemas.GeoMixinDeserializerSchema,
        schemas.EtlDataMixinDeserializerSchema,
        schemas.MetaBaseDeserializerSchema):
    """A default deserializer implementation for shapefile data.
    """
    pass


class EtlEventMetaBaseDeserializer(
        schemas.GeoMixinDeserializerSchema,
        schemas.TimeMixinDeserializerSchema,
        schemas.EtlDataMixinDeserializerSchema,
        schemas.MetaBaseDeserializerSchema):
    """A default deserializer implementation for ETL event data.
    """
    pass


class StreamingEventMetaBaseDeserializer(
        schemas.GeoMixinDeserializerSchema,
        schemas.TimeMixinDeserializerSchema,
        schemas.StreamingDataMixinDeserializerSchema,
        schemas.MetaBaseDeserializerSchema):
    """A default deserializer implementation for streaming event data.
    """
    pass


class EtlSensorNetEventMetaBaseDeserializer(
        schemas.GeoMixinDeserializerSchema,
        schemas.TimeMixinDeserializerSchema,
        schemas.EtlDataMixinDeserializerSchema,
        schemas.MetaBaseDeserializerSchema,
        schemas.SensorNetMixinDeserializerSchema):
    """A default deserializer implementation for ETL sensor event data.
    """
    pass


class StreamingSensorNetEventMetaBaseDeserializer(
        schemas.GeoMixinDeserializerSchema,
        schemas.TimeMixinDeserializerSchema,
        schemas.StreamingDataMixinDeserializerSchema,
        schemas.MetaBaseDeserializerSchema,
        schemas.SensorNetMixinDeserializerSchema):
    """A default deserializer implementation for streaming sensor event data.
    """
    pass
