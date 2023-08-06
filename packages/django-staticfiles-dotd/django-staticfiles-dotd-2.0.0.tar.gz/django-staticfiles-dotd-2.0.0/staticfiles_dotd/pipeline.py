import os

from django.conf import settings
from django.template import engines


def django_template_engine(filename, contents):
    if not os.path.splitext(filename)[1] in ('.html', '.css', '.js'):
        return contents

    template = engines['django'].from_string(contents.decode('utf-8'))

    return template.render({}).encode('utf-8')


def scss(filename, contents):
    if not filename.endswith('.scss'):
        return contents

    from scss.compiler import compile_string

    return compile_string(
        contents,
        output_style='legacy' if settings.DEBUG else 'compressed',
    ).encode('utf-8')
