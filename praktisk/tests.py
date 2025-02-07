from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage

from .models import FaqPage, InfoPage


class PraktiskSanityChecks(WagtailPageTestCase):
    def setUp(self):
        homePage = HomePage.objects.get()

        rootInfoPage = InfoPage(title="Random info index")
        homePage.add_child(instance=rootInfoPage)

        rootInfoPage.add_child(instance=InfoPage(title="Test info page"))
        rootInfoPage.add_child(instance=InfoPage(title="Unpublished info page", live=False))
        rootInfoPage.add_child(instance=FaqPage(title="Test faq page"))

    def test_info_pages_are_readable_via_code(self):
        self.assertIsNotNone(InfoPage.objects.filter(title="Test info page").first())
        self.assertIsNotNone(InfoPage.objects.filter(title="Unpublished info page").first())

    def test_info_page_is_readable_via_api(self):
        infoPage = InfoPage.objects.get(title="Test info page")
        response = self.client.get(f"/api/v2/info/{infoPage.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_unpublished_info_page_is_not_readable_via_api(self):
        infoPage = InfoPage.objects.get(title="Unpublished info page")
        response = self.client.get(f"/api/v2/info/{infoPage.pk}/")
        self.assertEqual(response.status_code, 404)

    def test_index_of_info_page_is_readable_via_api(self):
        response = self.client.get("/api/v2/info/")
        pages = response.json().get("items")
        self.assertEqual(len(pages), 3)  # 2 info pages and 1 faq page, 1 info page is unpublished

    def test_html_url_reflects_page_tree_slugs(self):
        self.assertEqual(InfoPage.objects.get(title="Test info page").get_url(), "/random-info-index/test-info-page/")
        self.assertEqual(FaqPage.objects.get(title="Test faq page").get_url(), "/random-info-index/test-faq-page/")


class PraktiskStructure(WagtailPageTestCase):
    def test_info_page_can_only_be_created_under_other_info_pages(self):
        self.assertAllowedParentPageTypes(InfoPage, {InfoPage, HomePage})

    def test_info_page_can_only_have_info_or_faq_pages_as_children(self):
        self.assertAllowedSubpageTypes(InfoPage, {InfoPage, FaqPage})

    def test_faq_page_can_only_be_created_under_info_pages(self):
        self.assertAllowedParentPageTypes(FaqPage, {InfoPage})

    def test_faq_page_can_not_have_any_children(self):
        self.assertAllowedSubpageTypes(FaqPage, set())
