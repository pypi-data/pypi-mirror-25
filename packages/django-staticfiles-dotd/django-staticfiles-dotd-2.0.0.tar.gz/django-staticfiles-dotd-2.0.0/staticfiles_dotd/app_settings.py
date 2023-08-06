from django.conf import settings

RENDER_PIPELINE = getattr(settings, 'STATICFILES_DOTD_RENDER_PIPELINE', ())

DIRECTORY_SUFFIX = getattr(
    settings,
    'STATICFILES_DOTD_DIRECTORY_SUFFIX',
    '.d',
)
