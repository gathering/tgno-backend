from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage

from .models import InfoIndexPage, InfoPage


class PraktiskSanityChecks(WagtailPageTestCase):
    def setUp(self):
        homePage = HomePage.objects.get()

        infoIndexPage = InfoIndexPage(title="Random info index")
        homePage.add_child(instance=infoIndexPage)

        infoPage = InfoPage(
            title="Test info page",
            intro="Test intro",
            body="Test body",
        )
        infoIndexPage.add_child(instance=infoPage)

        InfoPage(
            title="Secret info page",
            intro="This page isnt part of page tree",
            body="Test body",
            # Fake values, probably not possible using Wagtail page model.
            # A nice way of demoing behaviour and difference between API
            # endpoints and the "default" html endpoints, via tests below
            path="/",
            depth=1,
        ).save()

    def test_info_pages_are_readable_via_code(self):
        self.assertIsNotNone(InfoPage.objects.filter(title="Test info page").first())
        self.assertIsNotNone(InfoPage.objects.filter(title="Secret info page").first())

    def test_info_page_is_readable_via_api(self):
        infoPage = InfoPage.objects.get(title="Test info page")
        response = self.client.get(f"/api/v2/info/{infoPage.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_secret_info_page_is_not_readable_via_api(self):
        infoPage = InfoPage.objects.get(title="Secret info page")
        response = self.client.get(f"/api/v2/info/{infoPage.pk}/")
        self.assertEqual(response.status_code, 404)

    def test_index_of_info_page_is_readable_via_api(self):
        response = self.client.get("/api/v2/info/")
        pages = response.json().get("items")
        self.assertEqual(len(pages), 2)  # Lists both info and info index pages

    def test_html_url_reflects_page_tree_slugs(self):
        self.assertEqual(InfoPage.objects.get(title="Test info page").get_url(), "/random-info-index/test-info-page/")
        self.assertIsNone(InfoPage.objects.get(title="Secret info page").get_url())

    def test_info_page_api_details_contains_schedule(self):
        infoPage = InfoPage.objects.get(title="Test info page")
        response = self.client.get(f"/api/v2/info/{infoPage.pk}/")
        self.assertIsNotNone(response.json().get("meta").get("schedule"))


class PraktiskStructure(WagtailPageTestCase):
    def test_info_page_can_only_be_created_under_info_index_page(self):
        self.assertAllowedParentPageTypes(InfoPage, {InfoIndexPage})

    def test_info_page_index_can_only_have_info_or_index_pages_as_children(self):
        self.assertAllowedSubpageTypes(InfoIndexPage, {InfoPage, InfoIndexPage})
