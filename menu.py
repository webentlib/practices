from django.urls import reverse
from django.utils.module_loading import import_string


def item(
    path: str,
    name: str,
    target: str = None,
    description: str = None,
):
    # Если путь похож на модуль app_name.ClassName
    if (
        not path.startswith('/') and
        not path.startswith('http://') and
        not path.startswith('https://') and
        path.count('.') == 1
    ):
        app_label, model_name = path.split('.')
        # Causes import problems:
        # path = reverse('admin:%s_%s_changelist', (app_label, model_name.lower()))
        path = reverse('admin:index') + app_label + '/' + model_name.lower() + '/'
        if description is None:
            description = model_name

    item = {
        'path': path,
        'name': name,
        'target': target,
    }
    if description:
        item['description'] = description
    return item


def menu(request):
    from django.conf import settings
    DAOS_MENU = import_string(settings.DAOS_MENU)
    return {'DAOS_MENU': DAOS_MENU}
