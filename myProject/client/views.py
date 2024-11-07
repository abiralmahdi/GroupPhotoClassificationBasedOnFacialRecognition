from django.shortcuts import render, redirect ,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from home.models import Event, PicsRelation, userPicsRelation
import threading
import os
from django.conf import settings
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Create your views here.

def sharedEvent(request, eventID):
    event = Event.objects.get(id=eventID)
    if not event.published:
        return HttpResponse("<h1>Restricted access</h1>")
    

    pictures = PicsRelation.objects.filter(event=event)

    return render(request, 'clienteventPage.html',{'event':event, 'photos':pictures,'eventcode':event.code})
   
