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

2 In `settings.py` at the very top of your `# CUSTOM` block add:
```python
# Paths

TEMPLATES[0]['OPTIONS']['libraries'] = {}
STATICFILES_DIRS = []
FORMAT_MODULE_PATH = []

# Adm

from adm import patch_model_field_to_accept_group_param

ADM_MENU = 'stem.adm_menu.ADM_MENU'

TEMPLATES[0]['DIRS'] += ['adm/templates']
TEMPLATES[0]['OPTIONS']['libraries']['adm_extras'] = 'adm.templatetags.adm_extras'
TEMPLATES[0]['OPTIONS']['context_processors'] += ['adm.menu.menu']

STATICFILES_DIRS += [BASE_DIR / 'adm/static/']

FORMAT_MODULE_PATH += ['apps.adm.formats']
USE_THOUSAND_SEPARATOR = True
```

3. Change path of `ADM_MENU` to the path where your menu list actually placed.


# Key features

- Ускорены запросы, в случае если в списке есть возможность редактирования Foreign Key (проблема n+1);
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


# After any changes check:

## This pages
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

## This blocks
- Левая панель
- Хлебные крошки
- Вёрстка
- Мессаджи
- В светлой и тёмной темах
