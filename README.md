# Installation

1. Create somewhere list of admin menu items like:
`stem/adm_menu.py`:
```python
from adm.menu import item


ADM_MENU = [
    item('users/user/', 'Пользователи', 'User'),
    item('users/group/', 'Группы', 'Group'),
]
```

2 Add settings to `settings.py` at the very top of your `# CUSTOM`:
```python
# Paths

TEMPLATES[0]['OPTIONS']['libraries'] = {}
STATICFILES_DIRS = []
FORMAT_MODULE_PATH = []

# Adm

ADM_MENU = 'stem.adm_menu.ADM_MENU'

TEMPLATES[0]['DIRS'] += ['adm/templates']
TEMPLATES[0]['OPTIONS']['libraries']['adm_extras'] = 'adm.templatetags.adm_extras'
TEMPLATES[0]['OPTIONS']['context_processors'] += ['adm.menu.menu']

STATICFILES_DIRS += [BASE_DIR / 'adm/static/']

FORMAT_MODULE_PATH += ['apps.adm.formats']
USE_THOUSAND_SEPARATOR = True

# from adm import patch_model_field_to_accept_group_param  # uncomment to enable `group` param
```

Block `# Paths` is optional depending on how your project's `TEMPLATES`, `STATICFILES_DIRS` and `FORMAT_MODULE_PATH` vars are organized.

Change path of `ADM_MENU` and other settings to the path where your menu list and stuff actually placed.


# Common use cases

1. Now, all `ModelAdmins` inherited from `adm.admin.AdmModelAdmin` have 3 additional properties possible:
```python
from adm.admin import AdmModelAdmin
from apps.myapp.models import MyModel


@admin.register(MyModel)
class MyModelAdmin(AdmModelAdmin):
    list_select_related = []  # fields to `select_related` while in `list_editable`
    nowrap_fields = []        # columns to apply `white-space:nowrap` cc-rule
    additional_numeric_fields = []  # numeric columns added via `@staticmethod` must also be aligned to right
```

2. In addition, there is a convenient method to gather all `readonly_fields` with:
`readonly_fields = AdmModelAdmin.get_readonly(MyModel)`


# Additional use case (define `fieldsets` via `group` param)

Fieldsets can be defined like that:
```python
fieldsets = [
    [None, {
        'fields': AdmModelAdmin.get_group(MyModel, None)
    }],
    ['Counters', {
        'classes': ['collapse', 'open'],  # yes, 'open' now works properly with adm
        'fields': AdmModelAdmin.get_group(MyModel, 'COUNTERS'),
    }],
]
```

To make `.get_group(...)` method work — uncomment that line in `settings.py`:  
`# from adm import patch_model_field_to_accept_group_param  # uncomment to enable `group` param`

It makes all subclasses of `django.db.models.fields.Field` accept `group` attribute:
`count = models.IntegerField(group='COUNTERS')`


# Protect staff users from brute-force

The idea is to add a counter for failed attempts and drive it with custom admin auth form.

1. Inherit your 'User' from `adm.models.AdmUser`.
   Do not forget to migrate:
   $ python manage.py makemigrations
   $ python manage.py migrate
    
2. Add `site.py` somewhere in `stem` folder with following content:
```python
from django.contrib import admin
from adm.forms import AdmAuthenticationForm


class CustomAdminSite(admin.AdminSite):
    index_title = 'MyAdmin'
    login_form = AdmAuthenticationForm

```
3. Add `apps.py` also somewhere in `stem` folder with following content:
```python
from django.contrib import admin
from django.contrib.admin import sites
from django.contrib.admin.apps import AdminConfig


class CustomAdminConfig(AdminConfig):
    name = 'stem'

    def ready(self):
        """https://stackoverflow.com/a/30056258/4117781"""
        from stem.site import CustomAdminSite

        base_admin_site = CustomAdminSite()
        admin.site = sites.site = base_admin_site
```
4. Add this to the very top of `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = [
    # Custom admin
    'stem.apps.CustomAdminConfig',
    
    ...
]
```

Done


# How to override things

Assumes, that adm module will be installed in root dir.

1. To override python code — one can edit module itself, or create `adm` folder in `apps` and "inherit/extend".
2. To override templates — just specify another templates folder, to point it for example to root's templates `TEMPLATES[0]['DIRS'] += ['templates']` somewhere above `TEMPLATES[0]['DIRS'] += ['adm/templates']`. Then just create `admin` folder inside. 
3. To override static, similarly, one can specify something like `STATICFILES_DIRS = [BASE_DIR / 'static/']` above `STATICFILES_DIRS += [BASE_DIR / 'adm/static/']`.


# Key features

- Ускорены запросы, в случае если в списке есть возможность редактирования Foreign Key (проблема n+1);
- Защита от брутфорса сотрудников;
- Упрощены способы описания правил для генерации ui;
- Имеет и верхнее и боковое меню;
- Заголовки таблиц прилипают к экрану;
- Шапка и футер прилипают к экрану;
- Селекты имеют поиск, и множественный выбор (Select2);
- Все числа прижимаются к правому краю, числа разделяются пробелами каждые 3 знака и т.д. и т.п.;
- Минимизировано пустое бесполезное пространство (padding/margin и т.д.), перекомпанованы элементы поиска/добавления/действий в списке материалов; вырезаны хлебные крошки там где они не нужны;
- Короткие и информативные заголовки и <title>;
- Все эти изменения адаптируется и под моб. устройства;
- и т.д. и т.п.


# What's done in details

### Шапка:
- Плавающая
- Левое меню перенесено в Шапку, и доступно н всех страницах
- Пользовательские действия вынесены из Шапки на главную страницу

### Список:
- actions / search / add — объединены в одну строку и плавают
- Шапка таблицы, а также первые две th каждой строки — плавают
- Фильтр — плавает
- Пагинация — плавает
- Возможность указать поля, с запретом переноса строк (white-space: nowrap)
- Все числа выровнены по правому краю
- Числа разделяются пробелом каждые 3 знака
- Дроби разделяются точкой, а не запятой

### Детальная Страница:
- Нижняя Панель с кнопками плавает 
- Шапка inline-таблиц, а также первые две th каждой строки — плавают (как в списке)
- Чекбоксы — вытянуты
- Уменьшены расстояния между блоками
- Исправлен баг сворачивания/раскрытия объединённых полей

### Контролы (актуально для Списка и Детальной Страницы):
- Контролы приведены к единому размеру
- Виджет дата/время в одну строку
- Select 2 (в т.ч. multiple)

### Прочее:
- Упрощён <title> на всех страница
- Фавиконка
- Хлебные крошки вынесены в заголовки
- Главная страница вытянута на всю ширину окна
- Мобильная версия — юзабельна


# After any overrides check:

### This pages
| Name  | Link |
| --- | --- |
| Дашборд                             | http://127.0.0.1:8000/admin/                           |                                                                          
| Страница апликейшена                | http://127.0.0.1:8000/admin/users/                     |                                                    
| Список: С фильтром                  | http://127.0.0.1:8000/admin/users/user/                |                                                               
| Список: С редактируемыми полями     | http://127.0.0.1:8000/admin/users/group/               |                                               
| Список: Подтверждение удаления      | http://127.0.0.1:3000/admin/users/user/                |                                              
| Детальная: Страница добавления      | http://127.0.0.1:8000/admin/users/user/add/            |                                                  
| Детальная: С филдсетами             | http://127.0.0.1:3000/admin/users/user/1/change/       |                                                               
| Детальная: Простая                  | http://127.0.0.1:3000/admin/users/user/2/change/       |                                                        
| Детальная: История                  | http://127.0.0.1:3000/admin/users/user/1/history/      |                                                        
| Детальная: Подтверждение удаления   | http://127.0.0.1:3000/admin/users/user/1/delete/       |                                                       
| Пользователь: Вход для анонимного   | http://127.0.0.1:8000/admin/                           |                                   
| Пользователь: Сброс пароля          | http://127.0.0.1:3000/admin/users/user/1/password/     |                                                         
| Пользователь: Смена пароля          | http://127.0.0.1:3000/admin/password_change/           |                                                               
| Пользователь: Выход                 | http://127.0.0.1:3000/admin/logout/                    |                                          
| Документация: Главная               | http://127.0.0.1:8000/admin/doc/                       |                                       
| Документация: Список                | http://127.0.0.1:8000/admin/doc/models/                |                                              
| Документация: Детальная страница    | http://127.0.0.1:8000/admin/doc/models/admin.logentry/ |                                                             

### And this blocks
- Левая панель
- Хлебные крошки
- Вёрстка
- Мессаджи
- В светлой и тёмной темах
