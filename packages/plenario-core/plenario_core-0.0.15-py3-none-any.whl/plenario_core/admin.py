from django.contrib.gis import admin


_date_hierarchy = 'date_created'

_default_lat = 41.881832
_default_lon = -87.632177
_default_zoom = 5

_list_display = [
    'name', 'contributor', 'date_created', 'date_updated',
    'ds_first_run_date', 'ds_last_run_date'
]

_search_fields = ['name']

_meta_base_fields = [
    'name', 'contributor', 'slug', 'description', 'attribution',
    'date_created', 'date_updated', 'ds_first_run_date', 'ds_last_run_date',
    'ds_source_fields',
]
_meta_base_readonly_fields = [
    'slug', 'date_created', 'date_updated', 'ds_first_run_date',
    'ds_last_run_date',
]

_etl_data_fields = [
    'source_url', 'refresh_rate', 'refresh_interval', 'refresh_starts_on',
    'last_refreshed', 'next_refresh', 'state',
]
_etl_data_readonly_fields = [
    'last_refreshed', 'next_refresh', 'state',
]

_streaming_data_fields = [
    '_token', 'is_relayed', 'state',
]
_streaming_data_readonly_fields = [
    '_token', 'state',
]

_geo_fields = ['ds_srid', 'ds_bbox', 'ds_configured_point_fields']
_geo_readonly_fields = ['ds_bbox']

_time_fields = ['ds_timezone', 'ds_timerange', 'ds_configured_date_fields']
_time_readonly_fields = ['ds_timerange']

_sensor_net_fields = ['nodes']


class ShapeMetaBaseAdmin(admin.GeoModelAdmin):
    """A basic ModelAdmin for shapefile data.
    """

    date_hierarchy = _date_hierarchy
    default_lat = _default_lat
    default_lon = _default_lon
    default_zoom = _default_zoom
    list_display = _list_display
    search_fields = _search_fields
    fields = _meta_base_fields + _etl_data_fields + _geo_fields
    readonly_fields = _meta_base_readonly_fields + \
        _etl_data_readonly_fields + \
        _geo_readonly_fields


class EtlEventMetaBaseAdmin(admin.GeoModelAdmin):
    """A basic ModelAdmin for ETL event data.
    """

    date_hierarchy = _date_hierarchy
    default_lat = _default_lat
    default_lon = _default_lon
    default_zoom = _default_zoom
    list_display = _list_display
    search_fields = _search_fields
    fields = _meta_base_fields + _etl_data_fields + _geo_fields + _time_fields
    readonly_fields = _meta_base_readonly_fields + \
        _etl_data_readonly_fields + \
        _geo_readonly_fields + \
        _time_readonly_fields


class StreamingEventMetaBaseAdmin(admin.GeoModelAdmin):
    """A basic ModelAdmin for streaming event data.
    """

    date_hierarchy = _date_hierarchy
    default_lat = _default_lat
    default_lon = _default_lon
    default_zoom = _default_zoom
    list_display = _list_display
    search_fields = _search_fields
    fields = _meta_base_fields + \
        _streaming_data_fields + \
        _geo_fields + \
        _time_fields
    readonly_fields = _meta_base_readonly_fields + \
        _streaming_data_readonly_fields + \
        _geo_readonly_fields + \
        _time_readonly_fields


class EtlSensorNetEventMetaBaseAdmin(admin.GeoModelAdmin):
    """A basic ModelAdmin for ETL sensor event data.
    """

    date_hierarchy = _date_hierarchy
    default_lat = _default_lat
    default_lon = _default_lon
    default_zoom = _default_zoom
    list_display = _list_display
    search_fields = _search_fields
    fields = _meta_base_fields + \
        _etl_data_fields + \
        _geo_fields + \
        _time_fields + \
        _sensor_net_fields
    readonly_fields = _meta_base_readonly_fields + \
        _etl_data_readonly_fields + \
        _geo_readonly_fields + \
        _time_readonly_fields


class StreamingSensorNetEventMetaBaseAdmin(admin.GeoModelAdmin):
    """A basic ModelAdmin for streaming sensor data.
    """

    date_hierarchy = _date_hierarchy
    default_lat = _default_lat
    default_lon = _default_lon
    default_zoom = _default_zoom
    list_display = _list_display
    search_fields = _search_fields
    fields = _meta_base_fields + \
        _streaming_data_fields + \
        _geo_fields + \
        _time_fields + \
        _sensor_net_fields
    readonly_fields = _meta_base_readonly_fields + \
        _streaming_data_readonly_fields + \
        _geo_readonly_fields + \
        _time_readonly_fields
