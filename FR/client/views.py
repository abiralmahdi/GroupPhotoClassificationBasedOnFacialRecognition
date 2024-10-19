from django.shortcuts import render, redirect
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



def checkSimilarImages(user, event):
    event_ = Event.objects.get(id=event)
    pics = PicsRelation.objects.filter(event=event_)
    profilePic = user.profilepicture
    picsArr = []
    
    for pic in pics:
        image_path = os.path.join(settings.MEDIA_ROOT, str(pic.image))
        picsArr.append(image_path)
    for pic in picsArr:
        result = recognize(profilePic, pic)
        if result:
            imgPath = os.path.relpath(result, settings.MEDIA_ROOT)
            relevantPic = PicsRelation.objects.get(image=imgPath.replace('\\','/'))
    
       
    
            userPics = userPicsRelation(image=relevantPic)
            userPics.save()
            userPics.user.add(user)



def sharedEvent(request, eventID):
    thread = threading.Thread(target=checkSimilarImages, args=(request.user, eventID))
    thread.start()
    event = Event.objects.get(id=eventID)
    pictures = PicsRelation.objects.filter(event=event)
    return render(request, 'clienteventPage.html',{'event':event, 'photos':pictures})
   
