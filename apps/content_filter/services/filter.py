import re
from typing import Iterable

from apps.content_filter.models import Keyword


class ContentFilterService:
    __separators_regex = re.compile(r"[\n\t\r\-,.]")

    def __init__(self):
        self.__global_keywords = None
        self.__global_phrases = None

    @property
    def global_keywords(self) -> set[str]:
        if self.__global_keywords is None:
            keywords = Keyword.objects.filter(telegram_channels__isnull=True)
            self.__global_keywords = set(keywords.values_list('text', flat=True))
        return self.__global_keywords

    def filter_content(self, text: str, keywords: Iterable[str] = None) -> set[str]:
        if keywords is None:
            keywords = self.global_keywords
        else:
            keywords = set(keywords)

        tokens = self._split_words(text)
        matches = keywords.intersection(tokens)
        phrases_keywords = ({'split_text': self._split_words(k), 'original_text': k} for k in keywords)
        phrases = set(k['original_text'] for k in phrases_keywords if len(k['split_text']) > 1)
        for phrase in phrases:
            if phrase in text.lower():
                matches.add(phrase)

        return matches

    @classmethod
    def _split_words(cls, text):
        return re.sub(cls.__separators_regex, ' ', text.lower()).split(' ')
