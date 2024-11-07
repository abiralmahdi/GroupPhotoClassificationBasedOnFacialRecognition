from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('myEvents', views.myEvents, name='events'),
    path('myPhotos', views.myPhotos, name='myPhotos'),
    path('addEvents', views.addEvents, name='addEvents'),
    path('addPhotos/<str:eventID>', views.addPhotos, name='addPhotos'),
    path('myEvents/<str:eventID>', views.eventPage, name='eventPage'),
    path('eventsAsAGuest/<str:userID>', views.eventsAsAGuest, name='eventsAsAGuest'),
    path('triggerRecognition/<str:user>/<str:event>', views.checkSimilarImages, name='checkSimilarImages'),
    path('publishEvent/<str:eventID>', views.publishEvent, name='publishEvent'),
    path('checkEventStatus/<str:eventID>', views.checkEventStatus, name='checkEventStatus'),
    path('restrictEvent/<str:eventID>', views.restrictEvent, name='restrictEvent'),
]
