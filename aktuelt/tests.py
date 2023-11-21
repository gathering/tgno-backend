from wagtail.test.utils import WagtailPageTestCase

from .models import NewsIndexPage, NewsPage


class AktueltNewsPageStructure(WagtailPageTestCase):
    def test_news_page_can_only_be_created_under_news_index_page(self):
        self.assertAllowedParentPageTypes(NewsPage, {NewsIndexPage})

    def test_news_page_index_can_only_hace_news_pages_as_children(self):
        self.assertAllowedSubpageTypes(NewsIndexPage, {NewsPage})
