from django.core.management.base import BaseCommand
from treebeard.exceptions import NodeAlreadySaved
from wagtail.models import Page, Site

from aktuelt.models import NewsIndexPage, NewsPage
from home.models import HomePage

# python manage.py seed --mode=refresh

""" Insert and update data only """
MODE_REFRESH = "refresh"

""" Insert, update, and clear all existin entries from the related tables """
MODE_CLEAR = "clear"


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
            self.stdout.write(f"{child} likely already exists on {parent}. Skipping")

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

    def SeedAktuelt(self):
        homePage = HomePage.objects.get(title="Seeded content home")

        try:
            newsIndexPage = NewsIndexPage.objects.get(title="Seeded news index")
        except NewsIndexPage.DoesNotExist:
            newsIndexPage = NewsIndexPage(title="Seeded news index")
        self.add_child(homePage, newsIndexPage)

        NEWS_SEED_DATA = [
            dict(
                title="First news",
                intro="Test intro",
                body="Test body",
            ),
            dict(
                title="Second news",
                intro="Test intro",
                body="Test body",
            ),
            dict(
                title="Third news",
                intro="Test intro",
                body="Test body",
            ),
            dict(
                title="Forth news",
                intro="Test intro",
                body="Test body",
            ),
        ]

        for news in NEWS_SEED_DATA:
            try:
                newsPage = NewsPage.objects.get(title=news["title"])
            except NewsPage.MultipleObjectsReturned:
                newsPage = NewsPage.objects.filter(title=news["title"]).first()
            except NewsPage.DoesNotExist:
                newsPage = NewsPage(**news)
            self.add_child(newsIndexPage, newsPage)

    def run_clean(self, mode):
        self.stdout.write("Cleaning data")
        if mode == MODE_CLEAR:
            Site.objects.all().delete()  # Sounds a bit too dangerous?
            HomePage.objects.all().delete()
            NewsIndexPage.objects.all().delete()
            NewsPage.objects.all().delete()
        else:
            self.stdout.write("Running in refresh mode. No data cleaned.")

    def run_seed(self, mode):
        self.stdout.write("Seeding site and home data")
        self.SeedSite()
        self.stdout.write("Seeding aktuelt data")
        self.SeedAktuelt()
