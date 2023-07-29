import re

from django.core.cache import cache

from apps.content_filter.models import Keyword

separators_regex = re.compile(r"[\n\t\r\-,.]")


def filter_content(text, *, use_cache=False) -> set[str]:
    keywords = get_keywords(use_cache=use_cache)
    tokens = split_words(text)
    matches = keywords.intersection(tokens)

    phrases = get_phrases(use_cache=use_cache)
    for phrase in phrases:
        if phrase in text.lower():
            matches.add(phrase)

    return matches.union(matches)


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


def get_phrases(*, use_cache=True) -> set[str]:
    """
    Get set of all filter keywords

    :param use_cache: use cache or not
    :return:
    """
    cache_key = 'filter_phrases'
    phrases = cache.get(cache_key)
    if use_cache and phrases is not None:
        return phrases

    keywords = Keyword.objects.values_list('text', flat=True)
    keywords = ({'split_text': split_words(k), 'original_text': k} for k in keywords)
    phrases = set(k['original_text'] for k in keywords if len(k['split_text']) > 1)
    cache.set(cache_key, phrases, 600)
    return phrases


def split_words(text):
    return re.sub(separators_regex, ' ', text.lower()).split(' ')
