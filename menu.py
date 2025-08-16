def item(path, name, description=None):
    item = {
        'path': path,
        'name': name,
    }
    if description:
        item['description'] = description
    return item


def menu(request):
    from django.conf import settings
    from django.utils.module_loading import import_string

    ADM_MENU = import_string(settings.ADM_MENU)

    return {'ADM_MENU': ADM_MENU}
