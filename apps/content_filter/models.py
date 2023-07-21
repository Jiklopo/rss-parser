from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.abstact_models import UUIDModel, DateTimeModel


class Keyword(UUIDModel, DateTimeModel):
    text = models.CharField(_('Текст'), max_length=256, unique=True)

    def save(self, *args, **kwargs):
        self.text = self.text.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Ключевое слово')
        verbose_name_plural = _('Ключевые слова')
