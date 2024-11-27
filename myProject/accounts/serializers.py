from rest_framework import serializers
from ..client.models import User


class UserSerializer(serializers.ModelSerializer):
    profilepicture_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 
            'contact', 'profilepicture', 'profilepicture_url', 
            'is_active', 'is_staff', 'is_superuser'
        ]
        read_only_fields = ['is_active', 'is_staff', 'is_superuser']

    def get_profilepicture_url(self, obj):
        # Return full URL for the profile picture
        request = self.context.get('request')
        if obj.profilepicture and request:
            return request.build_absolute_uri(obj.profilepicture.url)
        return None
