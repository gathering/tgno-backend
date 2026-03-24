from rest_framework import serializers


class CompetitionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.CharField()
    description = serializers.CharField()
    signup_link = serializers.URLField()
    competition_type = serializers.SerializerMethodField()

    def get_competition_type(self, obj):
        if obj.competition_type:
            return {
                "id": obj.competition_type.id,
                "name": obj.competition_type.name,
                "group": obj.competition_type.group,
            }
        return None
