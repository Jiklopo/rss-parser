from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _, gettext

from apps.news.models import RssFeed, RssEntry
from apps.news.services import RssFeedParser


@admin.register(RssFeed)
class RssFeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'parsing_frequency', 'last_parsed')
    readonly_fields = ('last_parsed', 'etag')

    @admin.action(description=_('Спарсить'))
    def parse_feed(self, request, qs):
        rss_parser = RssFeedParser()
        for feed in qs:
            rss_parser.parse_rss_feed(feed)

    actions = [parse_feed]


@admin.register(RssEntry)
class RssEntryAdmin(admin.ModelAdmin):
    list_display = ['rss_feed', 'title', 'published', 'passed_filter', 'link_html']
    list_select_related = ['rss_feed']
    readonly_fields = ['published', 'external_id']

    list_filter = ['rss_feed', 'passed_filter', 'published']
    search_fields = ['title', 'summary']

    @admin.action(description=_('Ссылка'))
    def link_html(self, obj):
        read_text = gettext('Читать')
        return mark_safe(f'<a href="{obj.link}" target="_blank">{read_text}</a>')
