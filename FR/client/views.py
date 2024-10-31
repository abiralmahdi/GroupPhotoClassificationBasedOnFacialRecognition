from django.shortcuts import render, redirect ,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from home.models import Event, PicsRelation, userPicsRelation
from django.db import transaction
from django.contrib import messages
from home.FacialRecognition import testIndividual
import threading
import os
from django.conf import settings
from django.http import JsonResponse

# Create your views here.
def checkSimilarImages(request, eventID):
    event_ = Event.objects.get(id=eventID)
    pics = PicsRelation.objects.filter(event=event_)
    matchedPics = []
    if request.method == "POST":
        # Get list of uploaded files
        dp = request.FILES.get('photo')
        arrayOfGroupImages = []
        # Get paths for existing event pictures
        for pic in pics:
            image_path = os.path.join(settings.MEDIA_ROOT, str(pic.image))
            arrayOfGroupImages.append(image_path)
            # Assuming recognize is a function that returns the path of the recognized image or None
        result = testIndividual(dp, arrayOfGroupImages)
        for i in result:
            print(i)
        # Render the template with matched pictures
        return render(request, "clientImages.html", {'event': event_, 'photos': matchedPics})
    return render(request, "clientImages.html", {'event': event_})


def sharedEvent(request, eventID):
    thread = threading.Thread(target=checkSimilarImages, args=(request.user, eventID))
    thread.start()
    event = Event.objects.get(id=eventID)
    if not event.published:
        return HttpResponse("<h1>Restricted access</h1>")
    pictures = PicsRelation.objects.filter(event=event)
    return render(request, 'clienteventPage.html',{'event':event, 'photos':pictures})
   
