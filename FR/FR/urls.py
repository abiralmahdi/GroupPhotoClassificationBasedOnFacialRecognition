from django.contrib import admin
from django.urls import path
from django.urls import path, include




# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    
    path('accounts/', include('accounts.urls')), 
    path('api/', include('API.urls')), 

]

