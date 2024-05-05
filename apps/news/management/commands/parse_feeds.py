from datetime import timedelta, datetime

import pytz
from django.core.management import BaseCommand
from django.db.models import Case, When, F
from django.utils import timezone

from apps.news.choices import ParsingFrequency
from apps.news.models import RssFeed
from apps.news.services import RssFeedParser


class Command(BaseCommand):
    help = 'Run all required parsers based on last_parsed timestamp'

    def handle(self, *args, **options):
        rss_parser = RssFeedParser()
        feeds = self.get_feeds_for_parsing()
        for feed in feeds:
            rss_parser.parse_rss_feed(feed)

    @staticmethod
    def get_feeds_for_parsing():
        feeds = RssFeed.objects.filter(last_parsed__isnull=False).annotate(next_parse_time=Case(
            When(
                parsing_frequency=ParsingFrequency.HOURLY,
                then=F('last_parsed') + timedelta(hours=1)
            ),
            When(
                parsing_frequency=ParsingFrequency.DAILY,
                then=F('last_parsed') + timedelta(days=1)
            ),
            When(
                parsing_frequency=ParsingFrequency.WEEKLY,
                then=F('last_parsed') + timedelta(days=7)
            ),
            When(
                parsing_frequency=ParsingFrequency.MONTHLY,
                then=F('last_parsed') + timedelta(days=30)
            ),
            default=datetime(year=9000, month=1, day=1, tzinfo=pytz.UTC)
        ))
        feeds = feeds.filter(next_parse_time__lte=timezone.now())
        return feeds | RssFeed.objects.filter(last_parsed__isnull=True)
