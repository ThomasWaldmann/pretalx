from rest_framework.serializers import (
    CharField, ModelSerializer, SerializerMethodField,
)

from pretalx.person.models import SpeakerProfile, User


class SubmitterSerializer(ModelSerializer):
    biography = SerializerMethodField()

    def get_biography(self, obj):
        if self.context.get('request') and self.context['request'].event:
            profile = obj.profiles.filter(event=self.context['request'].event).first()
            if profile:
                return profile.biography
        return ''

    class Meta:
        model = User
        fields = (
            'code', 'name', 'biography'
        )


class SpeakerSerializer(ModelSerializer):
    code = CharField(source='user.code')
    name = CharField(source='user.name')
    submissions = SerializerMethodField()

    def get_submissions(self, obj):
        if self.context.get('request') and self.context['request'].is_orga:
            qs = obj.user.submissions.filter(event=obj.event)
        else:
            qs = obj.user.submissions.filter(event=obj.event, slots__in=obj.event.current_schedule.talks.all())
        return qs.values_list('code', flat=True)

    class Meta:
        model = SpeakerProfile
        fields = (
            'code', 'name', 'biography', 'submissions',
        )
