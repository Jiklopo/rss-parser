from django import forms

from apps.content_filter.models import Keyword
from django.utils.translation import gettext_lazy as _



class KeywordCreateForm(forms.ModelForm):
    keywords = forms.CharField(
        label=_('Ключевые слова'), widget=forms.Textarea(),
        help_text=_('Введите список ключевых слов для добавления в базу. '
                    'В качестве разделителя значение поля "Разделитель"')
    )
    delimiter = forms.CharField(
        label=_('Разделитель'), initial=';',
        help_text=_('Разделитель, использующийся для списка ключевых слов')
    )

    def save(self, commit=True):
        saved_keywords = set(Keyword.objects.values_list('text', flat=True))
        delimiter = self.cleaned_data['delimiter']
        keywords = set(kword.lower().strip() for kword in self.cleaned_data['keywords'].split(delimiter))
        keyword_objects = (Keyword(text=kword) for kword in keywords if kword and kword not in saved_keywords)
        Keyword.objects.bulk_create(keyword_objects)
        return Keyword.objects.first()

    class Meta:
        model = Keyword
        fields = ['keywords', 'delimiter']
