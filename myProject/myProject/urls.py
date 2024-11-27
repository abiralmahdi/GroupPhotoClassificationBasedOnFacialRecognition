from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import Api
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('client/', include('client.urls')), 
    path('accounts/', include('accounts.urls')), 

    #The api
    path('triggerRecognitionAPI/<str:user>/<str:event>/<str:mode>', Api.CheckSimilarImagesAPI.as_view(), name='checkSimilarImagesAPI'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)