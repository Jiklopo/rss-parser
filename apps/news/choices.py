from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ParsingFrequency(TextChoices):
    HOURLY = 'HOURLY', _('Раз в час')
    DAILY = 'DAILY', _('Раз в день')
    WEEKLY = 'WEEKLY', _('Раз в неделю')
    MONTHLY = 'MONTHLY', _('Раз в месяц')
