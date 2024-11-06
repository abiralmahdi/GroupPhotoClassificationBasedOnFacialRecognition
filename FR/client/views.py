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
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Create your views here.



def checkSimilarImages(request, eventID):
    event_ = Event.objects.get(id=eventID)
    pics = PicsRelation.objects.filter(event=event_)
    
    if request.method == "POST":
        # Get list of uploaded files
        uploaded_files = request.FILES.getlist('file')
        matched_pics = []  # To store userPicsRelation objects for matched images
        
        # Loop through each uploaded file
        for profilePic in uploaded_files:
            file_name = default_storage.save(f'temp/{profilePic.name}', ContentFile(profilePic.read()))
            profile_pic_path = os.path.join(settings.MEDIA_ROOT, file_name)
            
            # Loop through each picture from the event
            for pic in pics:
                image_path = os.path.join(settings.MEDIA_ROOT, str(pic.image))
                
                # Assuming 'recognize' function compares the images and returns a path if matched
                print(f"user: {profile_pic_path} \n froupimage {image_path}")
                result = recognize(profile_pic_path ,image_path)
                if result:
                    imgPath = os.path.relpath(result, settings.MEDIA_ROOT)
                    relevantPic = PicsRelation.objects.get(image=imgPath.replace('\\', '/'))

                    # Create or get userPicsRelation object
                    userPics, created = userPicsRelation.objects.get_or_create(image=relevantPic)

                    # Add the user to the userPicsRelation object (if not already added)
                    userPics.user.add(request.user)

                    # Collect the userPics object to send to the template
                    matched_pics.append(userPics)

        # Render the template with matched pictures
        return render(request, "clientImages.html", {'event': event_, 'photos': matched_pics})
    
    return render(request, "clientImages.html", {'event': event_})






def sharedEvent(request, eventID):
    thread = threading.Thread(target=checkSimilarImages, args=(request, eventID))
    thread.start()
    event = Event.objects.get(id=eventID)
    if not event.published:
        return HttpResponse("<h1>Restricted access</h1>")
    

    pictures = PicsRelation.objects.filter(event=event)

    return render(request, 'clienteventPage.html',{'event':event, 'photos':pictures,'eventcode':event.code})
   
