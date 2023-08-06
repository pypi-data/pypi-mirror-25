from .utils import monkeypatch
from .views import serve

monkeypatch(serve, 'django.contrib.staticfiles.views', 'serve')
