from django.contrib import admin
from django.contrib import admin
from .models import PicsRelation, Event, userPicsRelation, AnonymousUserPicsRelation

# Register your models here.
admin.site.register(PicsRelation)
admin.site.register(Event)
admin.site.register(userPicsRelation)
admin.site.register(AnonymousUserPicsRelation)
