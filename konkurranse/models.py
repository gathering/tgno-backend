from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from wagtail.snippets.models import register_snippet


@register_snippet
class CompetitionType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    group = models.CharField(
        max_length=20,
        choices=[
            ("creative", "Creative"),
            ("esport", "Esport"),
        ],
        help_text="Which main group this competition type belongs to",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("group"),
    ]

    class Meta:
        verbose_name = "Competition Type"
        verbose_name_plural = "Competition Types"
        ordering = ["group", "name"]

    def __str__(self):
        return self.name


class CompetitionCategoryPage(Page):
    page_description = "Competition category and overview page"
    subpage_types = ["konkurranse.Competition"]
    parent_page_types = ["home.HomePage"]

    description = models.TextField(blank=True, help_text="Description of this competition category")

    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]

    api_fields = [
        APIField("description"),
        APIField("competitions"),
    ]

    @property
    def competitions(self):
        """Return all child competitions"""
        from .serializers import CompetitionSerializer

        children = self.get_children().live().specific()
        return [CompetitionSerializer(child).data for child in children]


class Competition(Page):
    page_description = "A competition page"
    subpage_types = []
    parent_page_types = ["konkurranse.CompetitionCategoryPage"]

    competition_type = models.ForeignKey(
        "CompetitionType",
        on_delete=models.PROTECT,
        related_name="competitions",
        null=True,
        blank=True,
        help_text="The type of this competition",
    )
    description = models.TextField()
    signup_link = models.URLField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("competition_type"),
        FieldPanel("description"),
        FieldPanel("signup_link"),
        InlinePanel("competition_rule_sets", label="Rule Sets"),
        InlinePanel("competition_prizes", label="Prizes"),
    ]

    api_fields = [
        APIField("description"),
        APIField("signup_link"),
        APIField("category"),
        APIField("rule_sets"),
        APIField("prizes"),
    ]

    @property
    def category(self):
        """Return competition type details"""
        if self.competition_type:
            return {
                "id": self.competition_type.id,
                "name": self.competition_type.name,
                "group": self.competition_type.group,
            }
        return None

    @property
    def rule_sets(self):
        """Return ordered rule sets with their content"""
        return [
            {
                "id": crs.rule_set.id,
                "title": crs.rule_set.title,
                "rules": crs.rule_set.rules,
            }
            for crs in self.competition_rule_sets.select_related("rule_set").all()
        ]

    @property
    def prizes(self):
        """Return ordered prizes"""
        return [
            {
                "name": prize.name,
                "price": prize.price,
            }
            for prize in self.competition_prizes.all()
        ]


class CompetitionRuleSet(Orderable):
    competition = ParentalKey(Competition, on_delete=models.CASCADE, related_name="competition_rule_sets")
    rule_set = models.ForeignKey("RuleSet", on_delete=models.CASCADE, related_name="competition_links")

    panels = [
        FieldPanel("rule_set"),
    ]

    class Meta:
        unique_together = [["competition", "rule_set"]]

    def __str__(self):
        return f"{self.competition.title} - {self.rule_set.title}"


class Prize(Orderable):
    competition = ParentalKey(Competition, on_delete=models.CASCADE, related_name="competition_prizes")
    name = models.CharField(max_length=255, blank=True, help_text="Optional name (e.g., '1st place', 'Best Design')")
    price = models.CharField(max_length=255, help_text="Prize value (can be a number or text like 'Gaming PC')")

    panels = [
        FieldPanel("name"),
        FieldPanel("price"),
    ]

    def __str__(self):
        return f"{self.competition.title} - {self.name or 'Prize'}: {self.price}"


@register_snippet
class RuleSet(models.Model):
    title = models.CharField(max_length=255)
    rules = RichTextField(blank=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("rules"),
    ]

    class Meta:
        verbose_name = "Competition Rule"
        verbose_name_plural = "Competition Rules"

    def __str__(self):
        return self.title
