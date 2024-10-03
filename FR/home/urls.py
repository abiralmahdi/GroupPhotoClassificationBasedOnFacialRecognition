from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('myEvents', views.myEvents, name='events'),
    path('addEvents', views.addEvents, name='addEvents'),
]
