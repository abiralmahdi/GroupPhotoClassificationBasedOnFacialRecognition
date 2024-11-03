from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Event, PicsRelation, userPicsRelation
from django.contrib import messages
from .FacialRecognition import recognize
import threading
import os
from django.conf import settings


User = get_user_model()  # Correctly get the User model

@login_required
def index(request):
    users = User.objects.all()  # Removed the instantiation
    return render(request, 'index.html', {'users': users})

def myEvents(request):
    if request.user.is_authenticated:
        users = User.objects.all()  # Removed the instantiation
        events = Event.objects.filter(host=request.user)
        arrPics = []
        for event in events:
            try:
                arrPics.append(PicsRelation.objects.filter(event=event)[0])
            except:
                pass
        return render(request, 'events.html', {'events': events, 'users': users, 'pics':arrPics})
    else:
        return redirect("/")



def addEvents(request):
    if request.method == "POST":
        name = request.POST.get('eventName')
        description = request.POST.get('eventDescription')
        guest_ids = request.POST.getlist('guests')  # Get guest IDs as a list
        event_date = request.POST.get('date')
        host = request.user

        # Fetch the User objects corresponding to the guest IDs
        guests = User.objects.filter(id__in=guest_ids)

        # Create the Event instance
        event = Event.objects.create(name=name, description=description, event_date=event_date, host=host)

        # Set the guests for the event
        event.guest.set(guests)
        event.save()

        # Handle the uploaded pictures
        eventPics = request.FILES.getlist('files[]')  # Change the key to 'files[]' to match Dropzone

        # Save multiple event pictures in the PicsRelation model
        for file in eventPics:
            PicsRelation.objects.create(event=event, image=file)

        return redirect("/myEvents")

    # If it's not a POST request, redirect to the home page
    return redirect("/")

def checkSimilarImages(user, event):
    event_ = Event.objects.get(id=event)
    pics = PicsRelation.objects.filter(event=event_)
    profilePic = user.profilepicture
    picsArr = []
    
    for pic in pics:
        image_path = os.path.join(settings.MEDIA_ROOT, str(pic.image))
        picsArr.append(image_path)
    
    result = recognize([profilePic], picsArr)
    if result != False:
        imgPath = os.path.relpath(result, settings.MEDIA_ROOT)
        relevantPic = PicsRelation.objects.get(image=imgPath.replace('\\','/'))
    
        print(relevantPic.event)
    
        userPics = userPicsRelation(image=relevantPic)
        userPics.save()
        userPics.user.add(user)

    


def addPhotos(request, eventID):
    if request.method == "POST":
        event = Event.objects.get(id=eventID)
        eventPics = request.FILES.getlist('file')  # Change the key to 'file' to match Dropzone
       # Save multiple event pictures in the PicsRelation model
        for file in eventPics:
            PicsRelation.objects.create(event=event, image=file)
            print(f"Picture saved for event: {event.name}")
    return redirect("/myEvents/"+eventID)


def eventPage(request, eventID):
    event = Event.objects.get(id=eventID)
    pictures = PicsRelation.objects.filter(event=event)
    thread = threading.Thread(target=checkSimilarImages, args=(request.user, eventID))
    thread.start()
    return render(request, 'eventPage.html',{'event':event, 'photos':pictures})


def myPhotos(request):
    if request.user.is_authenticated:
        picsUser = userPicsRelation.objects.filter(user=request.user)
        events = Event.objects.filter(guest=request.user)
        picsEvent = PicsRelation.objects.filter(event__in=events)

        

        # for event in events:
        #     mydict = {f"{event.name}": []}  # Initialize a dictionary for each event

        #     for pic in pics:
        #         try:
        #             # Filter PicsRelation based on event and picture's image
        #             p = PicsRelation.objects.get(event=event, image=pic.image)
        #             mydict[f"{event.name}"].append(p)  # Append pic object to the event's list
        #         except PicsRelation.DoesNotExist:
        #             continue  # If no matching picture found, continue to the next iteration
            
        #     myArr.append(mydict)  # Append the dictionary to myArr

        # return render(request, 'myPhotos.html', {
        #     'users_': request.user, 
        #     'pics': pics, 
        #     'events': events, 
        #     'picsEvent': picsEvent, 
        #     'myArr': myArr  # Pass the constructed array to the template
        # })

        myBigArr = []
        for event in events:
            myArr = []
            for picUser in picsUser:
                pic = PicsRelation.objects.filter(event=event)
                if picUser.image in pic:
                    myArr.append(picUser)
            myBigArr.append([event, myArr])
        print(myBigArr)
        return render(request, 'myPhotos.html', {'myBigArr':myBigArr})

    else:
        return redirect("/")