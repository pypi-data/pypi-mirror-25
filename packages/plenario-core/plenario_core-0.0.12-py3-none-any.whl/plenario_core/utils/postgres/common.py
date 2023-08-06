import codecs

from django.template import Context, Template


def render_sql(path: str, context: dict) -> str:
    """Renders a SQL template as a string to be fed to a cursor for execution.

    :param path: the path to the template file
    :param context: the context to be interpolated with the template
    :return: the interpolated template
    """
    with codecs.open(path, mode='r', encoding='utf8') as fh:
        template = Template(fh.read())
    context = Context(context)
    return template.render(context)
