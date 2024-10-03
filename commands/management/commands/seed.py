from django.core.management.base import BaseCommand
from taggit.models import Tag
from treebeard.exceptions import NodeAlreadySaved
from wagtail.models import Page, Site

from aktuelt.constants import ContributionTypes
from aktuelt.models import Contributor, NewsIndexPage, NewsPage, NewsPageContributor
from home.models import HomePage

# python manage.py seed --mode=refresh

""" Insert and update data only """
MODE_REFRESH = "refresh"

""" Insert, update, and clear all existin entries from the related tables """
MODE_CLEAR = "clear"

""" Data to be inserted """

TAGS_DATA = [
    dict(name="News"),
    dict(name="Events"),
    dict(name="Announcements"),
    dict(name="Updates"),
]

CONTRIBUTORS_DATA = [
    dict(name="John Doe", default_contribution_type=ContributionTypes.TEXT),
    dict(name="Jane Doe", default_contribution_type=ContributionTypes.VIDEO),
    dict(name="Alice", default_contribution_type=ContributionTypes.AUDIO),
    dict(name="Bob", default_contribution_type=ContributionTypes.PHOTOGRAPHY),
]


def NEWS_SEED_DATA():
    return [
        [
            # First entry is the news item
            dict(
                title="First news",
                slug="seed-first-news",
                intro="Test intro",
                body="Test body",
            ),
            # Second are attributes that need to be handled separately
            dict(
                tags=["News", "Events"],
                contributors=[
                    NewsPageContributor(contributor=Contributor.objects.get(name="John Doe")),
                    NewsPageContributor(contributor=Contributor.objects.get(name="Jane Doe")),
                ],
            ),
        ],
        [
            dict(
                title="Second news",
                slug="seed-second-news",
                intro="Test intro",
                body="Test body",
            ),
            dict(
                tags=["Announcements", "Updates"],
                contributors=[],
            ),
        ],
        [
            dict(
                title="Third news",
                slug="seed-third-news",
                intro="Test intro",
                body="Test body",
            ),
            dict(
                tags=["News"],
                contributors=[
                    NewsPageContributor(contributor=Contributor.objects.get(name="John Doe")),
                    NewsPageContributor(
                        contributor=Contributor.objects.get(name="Alice"), contribution_type="Audio and video"
                    ),
                ],
            ),
        ],
        [
            dict(
                title="Forth news",
                slug="seed-forth-news",
                intro="Test intro",
                body="Test body",
            ),
            dict(
                tags=["Announcements", "News"],
                contributors=[
                    NewsPageContributor(contributor=Contributor.objects.get(name="Bob")),
                ],
            ),
        ],
        [
            dict(
                title="Fifth news",
                slug="seed-fifth-news",
                intro="Test intro",
                body="Test body",
            ),
            dict(
                tags=[],
                contributors=[],
            ),
        ],
    ]


class Command(BaseCommand):
    help = "seed database for local development."

    def add_arguments(self, parser):
        parser.add_argument("--mode", type=str, help="Mode", default=MODE_REFRESH)

    def handle(self, *args, **options):
        self.run_clean(options["mode"])
        self.run_seed(options["mode"])

    def add_child(self, parent, child):
        try:
            parent.add_child(instance=child)
        except NodeAlreadySaved:
            self.stdout.write(f"{child} likely already exists on {parent}. Only saving changes to page itself.")
            child.save()

    def SeedSite(self):
        rootPage = Page.objects.get(slug="root")

        try:
            homePage = HomePage.objects.get(title="Seeded content home")
        except HomePage.DoesNotExist:
            homePage = HomePage(
                title="Seeded content home",
                body="Welcome to the site",
            )
        self.add_child(rootPage, homePage)

        try:
            site = Site.objects.get(is_default_site=True)
        except Site.DoesNotExist:
            site = Site(
                is_default_site=True,
                hostname="localhost",
                site_name="localhost",
                port=8000,
            )

        # Make sure our home page is used so that seeded content shows up
        site.root_page = homePage
        site.save()

    def SeedTags(self):
        for tag in TAGS_DATA:
            Tag.objects.update_or_create(
                name=tag["name"],
                defaults=tag,
            )

    def SeedContributors(self):
        for contributor in CONTRIBUTORS_DATA:
            Contributor.objects.update_or_create(
                name=contributor["name"],
                defaults=contributor,
            )

    def SeedAktuelt(self):
        homePage = HomePage.objects.get(title="Seeded content home")

        try:
            newsIndexPage = NewsIndexPage.objects.get(title="Seeded news index")
        except NewsIndexPage.DoesNotExist:
            newsIndexPage = NewsIndexPage(title="Seeded news index")
        self.add_child(homePage, newsIndexPage)

        for raw_news in NEWS_SEED_DATA():
            news, meta = raw_news
            try:
                newsPage = NewsPage.objects.get(slug=news["slug"])
            except NewsPage.MultipleObjectsReturned:
                newsPage = NewsPage.objects.filter(slug=news["slug"]).first()
            except NewsPage.DoesNotExist:
                newsPage = NewsPage()

            for key in news:
                setattr(newsPage, key, news[key])

            newsPage.tags.set(meta["tags"])
            newsPage.news_page_contributors.set(meta["contributors"])

            self.add_child(newsIndexPage, newsPage)

    def run_clean(self, mode):
        if mode == MODE_CLEAR:
            self.stdout.write("Clearing data")
            Site.objects.all().delete()  # Sounds a bit too dangerous?
            HomePage.objects.all().delete()
            Tag.objects.all().delete()
            Contributor.objects.all().delete()
            NewsIndexPage.objects.all().delete()
            NewsPage.objects.all().delete()
        else:
            self.stdout.write("Running in refresh mode. No data cleared.")

    def run_seed(self, mode):
        self.stdout.write("Seeding site and home data")
        self.SeedSite()
        self.stdout.write("Seeding aktuelt data")
        self.SeedTags()
        self.SeedContributors()
        self.SeedAktuelt()
