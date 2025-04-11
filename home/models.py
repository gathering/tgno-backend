from django.core.exceptions import ValidationError
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page


class CtaBlock(blocks.StructBlock):
    text = blocks.CharBlock(label="Text", required=False)
    button_text = blocks.CharBlock(label="Button text", required=False)
    button_url = blocks.URLBlock(label="Button url", required=False)

    def clean(self, value):
        result = super().clean(value)
        button_filled_out = result["button_text"] or result["button_url"]
        complete_button = result["button_text"] and result["button_url"]

        if button_filled_out and not complete_button:
            raise blocks.StructBlockValidationError(
                block_errors={
                    "button_text": ValidationError("If you want to use CTA, both button text and url are required"),
                    "button_url": ValidationError("If you want to use CTA, both button text and url are required"),
                }
            )
        return result

    class Meta:
        label = "Call to action"


class HeroBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock(page_type=["aktuelt.NewsPage", "praktisk.InfoPage"])
    cta = CtaBlock()

    class Meta:
        label = "Hero section"
        icon = "placeholder"


class HomePage(Page):
    body = RichTextField(blank=True)
    # A bit overkill for current use. But nice example for later, and might trigger more ideas
    content = StreamField(
        [
            (
                "hero",
                HeroBlock(),
            ),
        ],
        null=True,
        blank=True,
        use_json_field=True,
        block_counts={"hero": {"max_num": 1, "min_num": 0}},
    )

    api_fields = [
        APIField("content"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]
