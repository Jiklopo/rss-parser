import re

from django.core.cache import cache

from apps.content_filter.models import Keyword

separators_regex = re.compile(r"[\n\t\r]")


def filter_content(text, *, use_cache=False) -> set[str]:
    keywords = get_keywords(use_cache=use_cache)
    text = re.sub(separators_regex, ' ', text.lower())
    tokens = (t.strip() for t in text.split(sep=' '))
    return keywords.intersection(tokens)


def get_keywords(*, use_cache=True) -> set[str]:
    """
    Get set of all filter keywords

    :param use_cache: use cache or not
    :return:
    """
    cache_key = 'filter_keywords'
    keywords = cache.get(cache_key)
    if use_cache and keywords is not None:
        return keywords

    keywords = set(Keyword.objects.values_list('text', flat=True))
    cache.set(cache_key, keywords, 600)
    return keywords
