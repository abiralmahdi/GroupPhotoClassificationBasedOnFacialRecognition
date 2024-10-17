from django.urls import path
from . import views

urlpatterns = [
    path('sharedEvent/<str:eventID>', views.sharedEvent, name='events'),
]
