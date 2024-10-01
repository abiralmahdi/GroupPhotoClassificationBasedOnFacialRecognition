from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from API.views import UserViewSet, PictureViewSet, EventViewSet, PicsRelationViewSet ,EventByHostView,EventGuestView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'pictures', PictureViewSet)
router.register(r'events', EventViewSet)
router.register(r'picsrelations', PicsRelationViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/events/host/<int:user_id>/', EventByHostView.as_view(), name='events_by_host'),
    path('api/events/guest/<int:user_id>/', EventGuestView.as_view(), name='events_by_host'),

    path('accounts/', include('accounts.urls')), 
]

