from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage

from .models import NewsIndexPage, NewsPage


class AktueltSanityChecks(WagtailPageTestCase):
    def setUp(self):
        homePage = HomePage.objects.get()

        newsIndexPage = NewsIndexPage(title="Random news index")
        homePage.add_child(instance=newsIndexPage)

        newsPage = NewsPage(
            title="Test news page",
            intro="Test intro",
            body="Test body",
            custom_published_at="2021-01-01T00:00:00Z",
        )
        newsIndexPage.add_child(instance=newsPage)

        NewsPage(
            title="Secret news page",
            intro="This page isnt part of page tree",
            body="Test body",
            # Fake values, probably not possible using Wagtail page model.
            # A nice way of demoing behaviour and difference between API
            # endpoints and the "default" html endpoints, via tests below
            path="/",
            depth=1,
        ).save()

    def test_news_pages_are_readable_via_code(self):
        self.assertIsNotNone(NewsPage.objects.filter(title="Test news page").first())
        self.assertIsNotNone(NewsPage.objects.filter(title="Secret news page").first())

    def test_news_page_is_readable_via_api(self):
        newsPage = NewsPage.objects.get(title="Test news page")
        response = self.client.get(f"/api/v2/news/{newsPage.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_secret_news_page_is_not_readable_via_api(self):
        newsPage = NewsPage.objects.get(title="Secret news page")
        response = self.client.get(f"/api/v2/news/{newsPage.pk}/")
        self.assertEqual(response.status_code, 404)

    def test_index_of_news_page_is_readable_via_api(self):
        response = self.client.get("/api/v2/news/")
        pages = response.json().get("items")
        self.assertEqual(len(pages), 1)

    def test_html_url_reflects_page_tree_slugs(self):
        self.assertEqual(NewsPage.objects.get(title="Test news page").get_url(), "/random-news-index/test-news-page/")
        self.assertIsNone(NewsPage.objects.get(title="Secret news page").get_url())

    def test_news_page_html_is_readable_via_page_url(self):
        newsPage = NewsPage.objects.get(title="Test news page")
        response = self.client.get(newsPage.get_url() or "/invalid-url/")
        self.assertEqual(response.status_code, 200)

    def test_secret_news_page_html_is_not_readable_via_page_url(self):
        newsPage = NewsPage.objects.get(title="Secret news page")
        response = self.client.get(newsPage.get_url() or "/invalid-url/")
        self.assertEqual(response.status_code, 404)

    def test_news_page_api_details_contains_custom_published_at(self):
        newsPage = NewsPage.objects.get(title="Test news page")
        response = self.client.get(f"/api/v2/news/{newsPage.pk}/")
        self.assertIsNotNone(response.json().get("meta").get("custom_published_at"))


class AktueltNewsPageStructure(WagtailPageTestCase):
    def test_news_page_can_only_be_created_under_news_index_page(self):
        self.assertAllowedParentPageTypes(NewsPage, {NewsIndexPage})

    def test_news_page_index_can_only_hace_news_pages_as_children(self):
        self.assertAllowedSubpageTypes(NewsIndexPage, {NewsPage})


class NewsPageBehaviour(WagtailPageTestCase):
    def setUp(self):
        self.newsPage = NewsPage(
            title="Test news page",
            intro="Test intro",
            body="Test body",
            path="/",
            depth=1,
        )
        self.newsPage.save()

    def test_publishing_is_empty_by_default(self):
        self.assertEqual(self.newsPage.first_published_at, None)
        self.assertEqual(self.newsPage.custom_published_at, None)
