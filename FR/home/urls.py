from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('myEvents', views.myEvents, name='events'),
    path('addEvents', views.addEvents, name='addEvents'),
    path('addPhotos/<str:eventID>', views.addPhotos, name='addPhotos'),
    path('myEvents/<str:eventID>', views.eventPage, name='eventPage'),
    path('triggerRecognition/<str:event>', views.triggerRecognition, name='triggerRecognition'),

]
