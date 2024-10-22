from django.shortcuts import render, redirect ,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from home.models import Event, PicsRelation, userPicsRelation
from django.db import transaction
from django.contrib import messages
from home.FacialRecognition import recognize
import threading
import os
from django.conf import settings
from django.http import JsonResponse

# Create your views here.



def checkSimilarImages(request, eventID):
    event_ = Event.objects.get(id=eventID)
    pics = PicsRelation.objects.filter(event=event_)
    
    if request.method == "POST":
        # Get list of uploaded files
        uploaded_files = request.FILES.getlist('file')
        picsArr = []

        # Get paths for existing event pictures
        for pic in pics:
            image_path = os.path.join(settings.MEDIA_ROOT, str(pic.image))
            picsArr.append(image_path)

        matched_pics = []  # To store userPicsRelation objects for matched images

        # Compare each uploaded file against existing pictures
        for profilePic in uploaded_files:
            for pic in picsArr:
                # Assuming recognize is a function that returns the path of the recognized image or None
                result = recognize(profilePic, pic)
                if result:
                    imgPath = os.path.relpath(result, settings.MEDIA_ROOT)
                    relevantPic = PicsRelation.objects.get(image=imgPath.replace('\\', '/'))

                    # Save the matching picture to userPicsRelation
                    userPic = userPicsRelation(image=relevantPic)
                    userPic.save()
                    
                    # Collect the userPic object to send to the template
                    matched_pics.append(userPic)

        # Render the template with matched pictures
        return render(request, "clientImages.html", {'event': event_, 'photos': matched_pics})
    
    return render(request, "clientImages.html", {'event': event_})



def sharedEvent(request, eventID):
    thread = threading.Thread(target=checkSimilarImages, args=(request.user, eventID))
    thread.start()
    event = Event.objects.get(id=eventID)
    if not event.published:
        return HttpResponse("<h1>Restricted access</h1>")
    pictures = PicsRelation.objects.filter(event=event)
    return render(request, 'clienteventPage.html',{'event':event, 'photos':pictures})
   
