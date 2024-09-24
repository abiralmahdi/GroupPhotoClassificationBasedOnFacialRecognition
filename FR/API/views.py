from django.shortcuts import render

from rest_framework import viewsets
from .models import User, Picture, Event, PicsRelation
from .serializers import UserSerializer, PictureSerializer, EventSerializer, PicsRelationSerializer


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

