import os.path
from typing import Union

from django.db import connection, transaction

from plenario_core.utils.postgres.common import render_sql


_sql_template_dir = os.path.join(os.path.dirname(__file__), 'sql')

_parse_pt_location_path = os.path.join(
    _sql_template_dir, 'parse-point-location.sql.template')
_parse_pt_lat_long_path = os.path.join(
    _sql_template_dir, 'parse-point-long-lat.sql.template')
_insert_pt_path = os.path.join(
    _sql_template_dir, 'insert-point.sql.template')
_create_trigger_path = os.path.join(
    _sql_template_dir, 'create-trigger.sql.template')


def add_point_triggers(meta_model: Union['GeoMixin', 'MetaBase']) -> None:
    """Adds functions and triggers to Postgres to handle parsing point data.

    :param meta_model: the data set model whose fields need to be parsed
    """
    table_name = meta_model.get_ds_table_name()

    # build parsing functions
    parse_fn_ctx = {
        'srid': meta_model.ds_srid,
    }
    parse_location_fn = render_sql(_parse_pt_location_path, parse_fn_ctx)
    parse_lat_long_fn = render_sql(_parse_pt_lat_long_path, parse_fn_ctx)

    # build insert function
    insert_fn_ctx = {
        'function_name': f'fn_{table_name}_point_insert',
        'location_fields': meta_model.ds_configured_point_fields,
    }
    insert_fn = render_sql(_insert_pt_path, insert_fn_ctx)

    # build trigger
    create_trigger_ctx = {
        'trigger_name': f'tgr_{table_name}_point_insert',
        'table_name': table_name,
        'procedure_name': insert_fn_ctx['function_name'],
    }
    create_trigger = render_sql(_create_trigger_path, create_trigger_ctx)

    # run in order as single transaction
    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute(parse_location_fn)
            cursor.execute(parse_lat_long_fn)
            cursor.execute(insert_fn)
            cursor.execute(create_trigger)
