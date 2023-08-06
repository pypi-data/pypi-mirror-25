from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.module_loading import import_string


def search(request):
    backend_class = import_string(settings.PCART_SEARCH_BACKEND)
    backend = backend_class(request)
    return backend.search_view()


def quick_search(request):
    backend_class = import_string(settings.PCART_SEARCH_BACKEND)
    backend = backend_class(request)
    return backend.quick_search_view()

