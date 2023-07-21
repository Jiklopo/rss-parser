from django.contrib import admin

from apps.content_filter.forms import KeywordCreateForm
from apps.content_filter.models import Keyword


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ['text', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

    def get_form(self, request, obj=None, change=False, **kwargs):
        if obj is None:
            return KeywordCreateForm
        return super().get_form(request, obj, change, **kwargs)

    def save_related(self, request, form, formsets, change):
        pass
