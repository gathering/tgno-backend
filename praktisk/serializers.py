from wagtail.api.v2.serializers import Field, PageSerializer


# The more basic serializers as seen in aktuelt/serializers.py seem a lot
# more appropriate for current usage here. But hoping we can find a pattern where
# the Info(Index)Page is used to serialize. Ie. it uses and respects
# `.api_fields` and `.api_meta_fields` from the model similar to how it is done
# in PageAPIViewSet.
#
# Currently just left here for someone to play around with when/if they want
class ChildInfoPageSerializer(Field):
    def __init__(self, *args, **kwargs):
        kwargs.pop("context")
        super().__init__(*args, **kwargs)

    def to_representation(self, info_page):
        return {
            "id": info_page.pk,
            "title": info_page.title,
            "intro": info_page.intro,
        }


class ChildInfoIndexPagesSerializer(Field):
    def to_representation(self, pages):
        return [
            {
                "id": index_page.pk,
                "title": index_page.title,
                "intro": index_page.intro,
            }
            for index_page in pages.all()
        ]
