from rest_framework import serializers
from .models import Event, PicsRelation, userPicsRelation, AnonymousUserPicsRelation
from django.contrib.auth import get_user_model

User = get_user_model()


class EventSerializer(serializers.ModelSerializer):
    host = serializers.StringRelatedField()  # Display host username
    guest = serializers.StringRelatedField(many=True)  # Display guest usernames

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'description', 'host', 'guest', 
            'event_date', 'published', 'code'
        ]


class PicsRelationSerializer(serializers.ModelSerializer):
    event = serializers.StringRelatedField()  # Display event name
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PicsRelation
        fields = ['id', 'event', 'image', 'image_url', 'date']

    def get_image_url(self, obj):
        # Return full URL of the image
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class UserPicsRelationSerializer(serializers.ModelSerializer):
    image = PicsRelationSerializer()  # Nested serializer for PicsRelation
    user = serializers.StringRelatedField(many=True)  # Display usernames

    class Meta:
        model = userPicsRelation
        fields = ['id', 'image', 'user']


class AnonymousUserPicsRelationSerializer(serializers.ModelSerializer):
    image = PicsRelationSerializer()  # Nested serializer for PicsRelation
    event = serializers.StringRelatedField()  # Display event name

    class Meta:
        model = AnonymousUserPicsRelation
        fields = ['id', 'image', 'user', 'event']
