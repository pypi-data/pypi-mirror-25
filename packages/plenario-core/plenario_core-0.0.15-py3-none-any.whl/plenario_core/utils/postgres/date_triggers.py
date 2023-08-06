import os.path
from typing import Union

from django.db import connection, transaction

from plenario_core.utils.postgres.common import render_sql


_sql_template_dir = os.path.join(os.path.dirname(__file__), 'sql')

_parse_timestamp_path = os.path.join(
    _sql_template_dir, 'parse-timestamp.sql.template')
_insert_timestamp_path = os.path.join(
    _sql_template_dir, 'insert-timestamp.sql.template')
_create_trigger_path = os.path.join(
    _sql_template_dir, 'create-trigger.sql.template')


def add_date_triggers(meta_model: Union['TimeMixin', 'MetaBase']) -> None:
    """Adds functions and triggers to Postgres to handle parsing date data.

    :param meta_model: the data set model whose fields need to be parsed
    """
    table_name = meta_model.get_ds_table_name()

    # build parsing function
    parse_fn_ctx = {
        'timezone': meta_model.ds_timezone,
    }
    parse_timestamp_fn = render_sql(_parse_timestamp_path, parse_fn_ctx)

    # build insert function
    insert_fn_ctx = {
        'function_name': f'fn_{table_name}_date_insert',
        'date_fields': meta_model.ds_configured_date_fields,
    }
    insert_fn = render_sql(_insert_timestamp_path, insert_fn_ctx)

    # build trigger
    create_trigger_ctx = {
        'trigger_name': f'tgr_{table_name}_date_insert',
        'table_name': table_name,
        'procedure_name': insert_fn_ctx['function_name'],
    }
    create_trigger = render_sql(_create_trigger_path, create_trigger_ctx)

    # run in order as single transaction
    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute(parse_timestamp_fn)
            cursor.execute(insert_fn)
            cursor.execute(create_trigger)
