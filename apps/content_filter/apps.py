from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ContentFilterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.content_filter'
    verbose_name = _('Фильтрация контента')
