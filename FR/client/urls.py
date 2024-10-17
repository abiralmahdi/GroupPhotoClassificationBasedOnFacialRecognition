from django.urls import path
from . import views

urlpatterns = [
    path('', views.myEvents, name='myEvents'),
    path('sharedEvent', views.myEvents, name='events'),
]
