from datetime import datetime
from logging import getLogger
from typing import Optional

import feedparser
import pytz
from bs4 import BeautifulSoup
from django.db import transaction
from django.utils import timezone
from feedparser import FeedParserDict

from apps.content_filter.services import ContentFilterService
from apps.news.models import RssFeed, RssEntry
from apps.news.services.exceptions import RssFeedBozoError
from apps.telegram.services import send_bot_message

logger = getLogger(__name__)


class RssFeedParser:
    def __init__(self):
        self._content_filter = ContentFilterService()

    def parse_rss_feed(self, rss_feed: RssFeed) -> list[RssEntry]:
        logger.info(f'Parsing "{rss_feed.name} RSS feed...')
        data = feedparser.parse(rss_feed.url, etag=rss_feed.etag)
        if data.bozo:
            raise RssFeedBozoError(f'Failed to parse rss feed "{rss_feed.url}":\n{data.bozo_exception}')

        with transaction.atomic():
            entries = (self.__create_rss_entry(rss_feed, e) for e in data.entries)
            entries = [e for e in entries if e is not None]
            rss_feed.etag = getattr(data, 'etag', None)
            rss_feed.last_parsed = timezone.now()
            rss_feed.save()

        return entries

    def __create_rss_entry(self, rss_feed, entry_data: FeedParserDict) -> Optional[RssEntry]:
        try:
            entry = RssEntry.objects.get(rss_feed=rss_feed, external_id=entry_data.id)
            logger.warning(f'Rss entry already exists. {entry.id=}')
            return None
        except RssEntry.DoesNotExist:
            pass

        published = datetime(*entry_data.published_parsed[:6], tzinfo=pytz.UTC)
        entry = RssEntry(
            rss_feed=rss_feed,
            link=entry_data.link,
            title=self._clear_html(entry_data.title),
            summary=self._clear_html(entry_data.summary),
            published=published,
            external_id=entry_data.id
        )
        matched_words = self._content_filter.filter_content(entry.filter_text)
        entry.matched_words = ' '.join(matched_words)
        entry.passed_filter = bool(matched_words)
        entry.save()
        send_bot_message(
            f'RSS: {rss_feed.name}'
            f'{entry.title}\n'
            f'Совпадения: {", ".join(matched_words)}\n\n'
            f'{entry.summary}\n\n'
            f'<a href="{entry.link}">Читать</a>'
        )
        return entry

    @staticmethod
    def _clear_html(text: str) -> str:
        soup = BeautifulSoup(text, 'html.parser')
        clean_text = soup.get_text()
        return clean_text
