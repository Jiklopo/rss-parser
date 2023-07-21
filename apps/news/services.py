from datetime import datetime
from logging import getLogger

import feedparser
from bs4 import BeautifulSoup
from django.db import transaction
from django.utils import timezone

from apps.content_filter.services import filter_content
from apps.news.models import RssFeed, RssEntry, EntryTag

logger = getLogger(__name__)


def parse_rss_feed(rss_feed: RssFeed):
    logger.info(f'Parsing "{rss_feed.name} RSS feed...')
    data = feedparser.parse(rss_feed.url, etag=rss_feed.etag)
    if data.bozo:
        logger.error(f'Failed to parse rss feed "{rss_feed.url}":\n{data.bozo_exception}')
        return

    with transaction.atomic():
        entries = (create_rss_entry(rss_feed, e) for e in data.entries)
        entries = [e for e in entries if e is not None]
        rss_feed.etag = getattr(data, 'etag', None)
        rss_feed.last_parsed = timezone.now()
        rss_feed.save()

    return entries


def create_rss_entry(rss_feed, entry_data):
    tags_text = [t.term.strip().lower() for t in getattr(entry_data, 'tags', [])]

    try:
        entry = RssEntry.objects.get(rss_feed=rss_feed, external_id=entry_data.id)
        logger.warning(f'Rss entry already exists. {entry.id=}')
        return None
    except RssEntry.DoesNotExist:
        pass

    published = datetime(*entry_data.published_parsed[:6])
    entry = RssEntry.objects.create(
        rss_feed=rss_feed,
        link=entry_data.link,
        title=clear_html(entry_data.title),
        summary=clear_html(entry_data.summary),
        published=published,
        external_id=entry_data.id
    )
    tags = [EntryTag.objects.get_or_create(text=t)[0] for t in tags_text]
    entry.tags.set(tags)

    matched_words = filter_content(entry.filter_text)
    if matched_words:
        entry.matched_words = ' '.join(matched_words)
        entry.passed_filter = True
        entry.save()

    return entry


def clear_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    clean_text = soup.get_text()
    return clean_text
