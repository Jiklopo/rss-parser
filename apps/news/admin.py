from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _, gettext

from apps.news.models import RssFeed, RssEntry, EntryTag
from apps.news.services import parse_rss_feed


@admin.register(RssFeed)
class RssSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'parsing_frequency', 'last_parsed')
    readonly_fields = ('last_parsed', 'etag')

    @admin.action(description=_('Спарсить'))
    def parse_feed(self, request, qs):
        for sub in qs:
            parse_rss_feed(sub)

    actions = [parse_feed]


@admin.register(RssEntry)
class RssEntryAdmin(admin.ModelAdmin):
    list_display = ['rss_feed', 'title', 'published', 'passed_filter', 'link_html']
    readonly_fields = ['published', 'external_id', 'tags_text']

    list_filter = ['rss_feed', 'passed_filter', 'tags', 'published']
    search_fields = ['title', 'summary']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('rss_feed')
        qs = qs.prefetch_related('tags')
        return qs

    @admin.action(description=_('Ссылка'))
    def link_html(self, obj):
        read_text = gettext('Читать')
        return mark_safe(f'<a href="{obj.link}" target="_blank">{read_text}</a>')


@admin.register(EntryTag)
class EntryTagAdmin(admin.ModelAdmin):
    pass
