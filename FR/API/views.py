from rest_framework import status
from rest_framework import viewsets
from .models import User, Picture, Event, PicsRelation
from .serializers import UserSerializer, PictureSerializer, EventSerializer, PicsRelationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .serializers import EventSerializer

# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Picture ViewSet
class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

# Event ViewSet
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# PicsRelation ViewSet
class PicsRelationViewSet(viewsets.ModelViewSet):
    queryset = PicsRelation.objects.all()
    serializer_class = PicsRelationSerializer

class EventByHostView(APIView):
    def get(self, request, user_id):
        # Filter events where host's ID matches the given user_id
        events = Event.objects.filter(host=user_id)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class EventGuestView(APIView):
    def get(self, request, user_id):
        # Filter events where guests's ID matches the given user_id
        events = Event.objects.filter(guest=user_id)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)