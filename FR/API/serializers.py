from rest_framework import serializers
from .models import User, Picture, Event, PicsRelation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['imageid', 'uploader', 'image']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['eventid', 'guest', 'eventdate']

class PicsRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PicsRelation
        fields = ['id', 'picid', 'aid']
