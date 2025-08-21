from django.contrib import admin
from django.db import models


class FakeQueryset(list):
    """
    Для реализации кэшируемых полей в DaosModelAdmin.formfield_for_foreignkey необходим список,
    у которого есть метод .all() и ._prefetch_related_lookups (возвращаемое значение не интересно).
    """

    def all(self):
        return self.__class__(self)

    def _prefetch_related_lookups(self, *args, **kwargs):
        pass


class DaosModelAdmin(admin.ModelAdmin):
    list_select_related = []
    nowrap_fields = []
    additional_numeric_fields = []

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if self.list_select_related and \
           self.list_select_related not in [True, False] and \
           db_field.name in self.list_select_related:  # Do we really need such a complex check?
            db_field_name_cache = db_field.name + '_cache'
            cached_queryset = getattr(request, db_field_name_cache, None)
            if not cached_queryset:
                formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
                setattr(request, db_field_name_cache, FakeQueryset(formfield.queryset))
            else:
                kwargs['queryset'] = cached_queryset
                formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
            return formfield
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        return formfield

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['nowrap_fields'] = self.nowrap_fields
        extra_context['numeric_fields'] = self._get_numeric_fields()
        return super().changelist_view(request, extra_context=extra_context)

    def _get_numeric_fields(self):
        field_names = self.additional_numeric_fields
        for field in self.model._meta.get_fields():
            if field.__class__ in [
                models.FloatField,

                models.SmallIntegerField,
                models.IntegerField,
                models.BigIntegerField,

                models.PositiveSmallIntegerField,
                models.PositiveIntegerField,
                models.PositiveBigIntegerField,
            ]:
                field_names.append(field.name)
        return field_names

    @staticmethod
    def get_group(model, group_name):
        group = []
        for field in model._meta.get_fields():
            if field.name == model._meta.pk.name:
                continue
            if issubclass(type(field), (models.ManyToOneRel, models.ManyToManyRel,)):
                continue
            if hasattr(field, 'group') and field.group == group_name:
                group.append(field.name)
            elif not hasattr(field, 'group') and not group_name:
                group.append(field.name)
        return group

    @staticmethod
    def get_readonly(model):
        readonly_fields = []
        for field in model._meta.get_fields():
            if issubclass(type(field), (models.ManyToOneRel, models.ManyToManyRel)):
                continue
            if field.name == model._meta.pk.name:
                continue
            if not getattr(field, 'editable'):
                readonly_fields.append(field.name)
        return readonly_fields

