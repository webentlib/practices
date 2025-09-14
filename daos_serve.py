import site
from django.http import Http404
from django.views.static import serve
from django.conf import settings


def daos_serve(request, path, show_indexes=False):
    dirs = settings.STATICFILES_DIRS + [site.getsitepackages()[0] + '/django/contrib/admin/static/']
    for dir in dirs:
        try:
            return serve(request, path, document_root=dir, show_indexes=show_indexes)
        except Http404:
            pass
    raise Http404
