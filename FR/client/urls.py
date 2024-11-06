from django.urls import path
from .views import *

urlpatterns = [
    path('sharedEvent/<int:eventID>', sharedEvent, name='sharedEvent'),
     path('checksimilarity/<int:eventID>', checkSimilarImages, name='checksimilarity'),
    
]
