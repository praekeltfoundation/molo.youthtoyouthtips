from daterange_filter.filter import DateRangeFilter
from import_export import resources, fields

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template.defaultfilters import truncatechars

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)
from wagtail.contrib.modeladmin.views import IndexView

from molo.yourtips.admin import (
    YourTipsEntryAdmin
)
from molo.yourtips.models import (
    YourTipsEntry,
    YourTipsArticlePage
)


class DateFilter(DateRangeFilter):
    template = 'admin/yourtips/yourtips_date_range_filter.html'


class YourTipsEntriesResource(resources.ModelResource):
    exclude = ('id', '_convert', 'converted_article_page')

    class Meta:
        model = YourTipsEntry


class YourTipsEntriesModelAdminTemplate(IndexView):
    def post(self, request, *args, **kwargs):

        dataset = YourTipsEntriesResource().export()

        response = HttpResponse(dataset.csv, content_type="csv")
        response['Content-Disposition'] = \
            'attachment; filename=yourtips_entries.csv'
        return response

    def get_template_names(self):
        return 'admin/yourtips/model_admin_template.html'


class YourTipsEntriesModelAdmin(ModelAdmin):
    model = YourTipsEntry
    menu_label = 'Entries'
    menu_icon = 'edit'
    index_view_class = YourTipsEntriesModelAdminTemplate
    add_to_settings_menu = False
    list_display = [
        'tip', 'submission_date', 'user', 'optional_name',
        'allow_share_on_social_media', '_convert'
    ]
    list_filter = [('submission_date', DateFilter)]

    def _convert(self, obj, *args, **kwargs):
        if obj.converted_article_page:
            return (
                '<a href="/admin/pages/%d/edit/">Article Page</a>' %
                obj.converted_article_page.id)
        return (
            '<a href="/django-admin/yourtips/yourtipsentry'
            '/%d/convert/" class="addlink">Convert to article</a>' %
            obj.id)

    _convert.allow_tags = True
    _convert.short_description = ''

    def tip(self, obj, *args, **kwargs):
        return truncatechars(obj.tip_text, 30)


class YourTipsEntryPageResource(resources.ModelResource):
    tip = fields.Field()
    author = fields.Field()
    total_votes = fields.Field()

    class Meta:
        model = YourTipsArticlePage
        fields = (
            'id', 'title', 'total_votes', 'live',
            'tip', 'author', 'latest_revision_created_at'
        )
        export_order = (
            'id', 'title', 'live', 'tip', 'author',
            'total_votes', 'latest_revision_created_at'
        )

    @staticmethod
    def dehydrate_tip(articlepage):
        for block in articlepage.body:
            if block.block_type == 'paragraph':
                tip = str(block)
        return tip.replace('<p>', '').replace('</p>', '')

    @staticmethod
    def dehydrate_author(articlepage):
        for block in articlepage.body:
            if block.block_type == 'heading':
                tip = str(block)
        return tip.replace('By ', '')

    @staticmethod
    def dehydrate_total_votes(articlepage):
        return articlepage.vote_total


class YourTipsEntryPageModelAdminTemplate(IndexView):
    def post(self, request, *args, **kwargs):

        dataset = YourTipsEntryPageResource().export()

        response = HttpResponse(dataset.csv, content_type="csv")
        response['Content-Disposition'] = \
            'attachment; filename=yourtips_convertedarticles.csv'
        return response

    def get_template_names(self):
        return 'admin/yourtips/model_admin_template.html'


class YourTipsEntryPageModelAdmin(ModelAdmin, YourTipsEntryAdmin):
    model = YourTipsArticlePage
    menu_label = 'Tips'
    menu_icon = 'doc-full-inverse'
    index_view_class = YourTipsEntryPageModelAdminTemplate
    add_to_settings_menu = False
    list_display = [
        'title', 'latest_revision_created_at', 'vote_total',
        'number_of_shares', 'live', '_share_on_facebook'
    ]
    list_filter = [('latest_revision_created_at', DateFilter)]

    def get_queryset(self, request):
        qs = super(YourTipsEntryPageModelAdmin, self).get_queryset(request)
        main = request.site.root_page
        return qs.descendant_of(main)

    def _share_on_facebook(self, obj):
        # TODO Check if user allowed share and secure site
        tip_url = 'http://%s' % Site.objects.get_current().domain + reverse(
            'molo.yourtips:tip_share', args=[obj.id]
        )
        return '<a href="http://www.facebook.com/sharer.php?u=%s"' \
               ' class="addlink">Share on Facebook</a>' % tip_url

    _share_on_facebook.allow_tags = True
    _share_on_facebook.short_description = ''


class YourTipsAdminGroup(ModelAdminGroup):
    menu_label = 'YourTips'
    menu_icon = 'folder-open-inverse'
    menu_order = 400
    items = (
        YourTipsEntriesModelAdmin, YourTipsEntryPageModelAdmin
    )


modeladmin_register(YourTipsAdminGroup)
