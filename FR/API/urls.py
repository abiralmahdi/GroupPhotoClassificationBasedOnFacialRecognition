from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    PictureViewSet,
    EventViewSet,
    PicsRelationViewSet,
    EventByHostView,
    EventGuestView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'pictures', PictureViewSet)
router.register(r'events', EventViewSet)
router.register(r'pics-relations', PicsRelationViewSet)

# Define the urlpatterns list
urlpatterns = [
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/events/host/<int:user_id>/', EventByHostView.as_view(), name='events_by_host'),
    path('api/events/guest/<int:user_id>/', EventGuestView.as_view(), name='events_by_host'),

]