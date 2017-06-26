from molo.yourtips.models import YourTipsEntry, YourTipsEntryPage
from molo.yourtips.tests.base import BaseYourTipsTestCase


class TestAdminActions(BaseYourTipsTestCase):

    def test_convert_to_article(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        entry = YourTipsEntry.objects.create(
            user_name='Test',
            tip_text='test body',
            allow_share_on_social_media=True,
        )

        response = self.client.get(
            '/django-admin/yourtips/yourtipsentry/%d/convert/' % entry.id
        )
        article = YourTipsEntryPage.objects.get(title='Tip-%s' % entry.id)
        entry = YourTipsEntry.objects.get(pk=entry.pk)
        self.assertEquals(entry.converted_article_page, article)
        self.assertEquals(article.body.stream_data, [
            {"type": "paragraph", "value": entry.tip_text},
            {"type": "paragraph", "value": "By Test"}
        ])

        self.assertEquals(YourTipsEntryPage.objects.all().count(), 1)

        # second time it should redirect to the edit page
        response = self.client.get(
            '/django-admin/yourtips/yourtipsentry/%d/convert/' %
            entry.id)
        self.assertEquals(
            response['Location'],
            '/admin/pages/%d/edit/' % article.id)
        self.assertEquals(YourTipsEntryPage.objects.all().count(), 1)
