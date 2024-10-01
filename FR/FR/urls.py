from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from API.views import UserViewSet, PictureViewSet, EventViewSet, PicsRelationViewSet ,EventByHostView,EventGuestView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView



# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    
    path('accounts/', include('accounts.urls')), 
    path('api/', include('API.urls')), 

]

