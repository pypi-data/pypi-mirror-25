from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from django.conf import settings
from translation_server.models import *
from translation_server.forms import *


class CustomModelAdminMixin(object):
    def __init__(self, model, admin_site):

        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(CustomModelAdminMixin, self).__init__(model, admin_site)
        self.filter_horizontal = [field.name for field in model._meta.get_fields() if
                                  field.many_to_many and "reverse" not in str(type(field))]

        # get all fields that aren't related to another model
        self.search_fields = [field.name for field in model._meta.get_fields() if
                              not field.many_to_many and "Point" not in str(type(field)) and "related" not in str(
                                  type(field))]

        # get all languages installed on settings.py
        languages_list = [lang[0].replace("-", "_") for lang in settings.LANGUAGES]

        related_fields = []
        # get all fields that are related to another model
        for model_field in model._meta.get_fields():
            if not model_field.many_to_many and "related" in str(type(model_field)):
                for related_field in model_field.related_model._meta.get_fields():
                    # if the field have one of the fields from the 'related_fields_to_add' variable
                    # and one of the languages in the field name, add it to the search_fields
                    if any("_"+language_code in related_field.name for language_code in languages_list):
                        related_fields.append(model_field.name+"__"+related_field.name)
                        self.search_fields.append(model_field.name+"__"+related_field.name)

        self.search_fields.remove("id")


@admin.register(TranslationType)
class TranslationTypeAdmin(CustomModelAdminMixin, TabbedTranslationAdmin):
    def get_queryset(self, request):
        qs = super(TranslationTypeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.exclude(tag__startswith='DTS')

    class Media:
        import os
        js_dir = os.path.join(settings.STATIC_URL, 'admin/js')
        js = (
            js_dir + '/admin-translation-type.js',
        )


@admin.register(Translation)
class TranslationAdmin(CustomModelAdminMixin, TabbedTranslationAdmin):
    form = TranslationAdminForm
    fieldsets = (
        ('Translation type', {
            'fields': ('type', 'translations_url', 'translation_type_url', 'last_translation_tag_url')
        }),
        ('Primary info', {
            'fields': ('tag', 'text')
        }),
        ('Auxiliary info', {
            'fields': ('auxiliary_tag', 'auxiliary_text')
        }),
    )
    list_display = ('tag', 'type', 'text')

    class Media:
        import os
        js_dir = os.path.join(settings.STATIC_URL, 'admin/js')
        js = (
            js_dir + '/admin-translation.js',
        )

    def get_queryset(self, request):
        qs = super(TranslationAdmin, self).get_queryset(request)
        # if request.user.is_superuser:
        #     return qs
        return qs.exclude(tag__startswith='DTS')

