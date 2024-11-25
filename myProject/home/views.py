from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Event, PicsRelation, userPicsRelation, AnonymousUserPicsRelation
from django.shortcuts import get_object_or_404 
from django.contrib import messages
from .FacialRecognition import cropOut
import threading
import os
from django.conf import settings
from django.http import JsonResponse
import random
from django.http import HttpResponse
import os
import zipfile
from io import BytesIO

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
        return render(request, 'events.html', {'events': events, 'users': users, 'pics':arrPics, 'status':'host'})
    else:
        return redirect("/")


@login_required
def addEvents(request):
    if request.method == "POST":
        name = request.POST.get('eventName')
        description = request.POST.get('eventDescription')
        guest_ids = request.POST.getlist('guests')  # Get guest IDs as a list
        event_date = request.POST.get('date')
        host = request.user

        # Fetch the User objects corresponding to the guest IDs
        guests = User.objects.filter(id__in=guest_ids)
        code = random.randint(100000, 999999)

        # Create the Event instance
        event = Event.objects.create(name=name, description=description, event_date=event_date, host=host, code=code)

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



def checkSimilarImages(request, user=None, event=None, mode="guest"):
    # Validate event existence
    event_ = get_object_or_404(Event, id=event)
    pics = PicsRelation.objects.filter(event=event_)
    relevant_pics = []

    # Validate user parameter
    userr = None
    if user is not None:
        try:
            userr = User.objects.get(id=user)  # Attempt to fetch the user if provided
        except (User.DoesNotExist, ValueError):
            userr = None  # Safely handle invalid user IDs or 'None'

    # Host mode: File upload and recognition
    if mode == "host" and request.method == "POST":
        profilePic = request.FILES['uploadedPhoto']
        personName = request.POST.get('personName', 'recognized_pics')
        for pic in pics:
            image_path = os.path.join(settings.MEDIA_ROOT, str(pic.image))
            result = cropOut(image_path, profilePic)
            if result:
                relevantPic = PicsRelation.objects.get(image=str(pic.image).replace('\\', '/'))
                if relevantPic:
                    AnonymousUserPicsRelation.objects.create(user=personName, image=relevantPic, event=event_)

    # Guest mode
    elif mode == "guest":
        profilePic = None
        print(profilePic)
        if userr:  # If a valid user object exists
            profilePic = userr.profilepicture
            if profilePic:
                for pic in pics:
                    image_path = os.path.join(settings.MEDIA_ROOT, str(pic.image))
                    result = cropOut(image_path, profilePic)
                    if result:
                        relevantPic = PicsRelation.objects.get(image=str(pic.image).replace('\\', '/'))    
                        if relevantPic:
                            AnonymousUserPicsRelation.objects.create(user=request.user.username, image=relevantPic, event=event_)
        if not profilePic:  # If profilePic is not provided
            if request.method == "POST":
                profilePic = request.FILES['uploadedPhoto']
                print(profilePic)
        if profilePic:
            for pic in pics:
                image_path = os.path.join(settings.MEDIA_ROOT, str(pic.image))
                result = cropOut(image_path, profilePic)
                if result:
                    relevantPic = PicsRelation.objects.get(image=str(pic.image).replace('\\', '/'))
                    relevant_pics.append(image_path)

            if relevant_pics:
                # Create a zip file for download
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                    for file_path in relevant_pics:
                        zip_file.write(file_path, os.path.basename(file_path))
                zip_buffer.seek(0)

                response = HttpResponse(zip_buffer, content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="YourPics.zip"'
                return response

    return redirect("/")






def checkSimilarImages2(request, user=None, event=None, mode="guest"):
    recognizedPicsArr = []
    def threadWrapper(image_path, profilePic):
        result = cropOut(image_path, profilePic)
        recognizedPicsArr.append(result)
        

    # Validate event existence
    event_ = get_object_or_404(Event, id=event)
    pics = PicsRelation.objects.filter(event=event_)
    relevant_pics = []

    # Validate user parameter
    userr = None
    if user is not None:
        try:
            userr = User.objects.get(id=user)  # Attempt to fetch the user if provided
        except (User.DoesNotExist, ValueError):
            userr = None  # Safely handle invalid user IDs or 'None'

    # Host mode: File upload and recognition
    if mode == "host" and request.method == "POST":
        profilePic = request.FILES['uploadedPhoto']
        personName = request.POST.get('personName', 'recognized_pics')
        threads = []
        for pic in pics:
            image_path = os.path.join(settings.MEDIA_ROOT, str(pic.image))
            thread = threading.Thread(target=threadWrapper, args=(image_path, profilePic, recognizedPicsArr))
            threads.append(thread)
            thread.start()  # Start the thread
            if result:
                relevantPic = PicsRelation.objects.get(image=str(pic.image).replace('\\', '/'))
                if relevantPic:
                    AnonymousUserPicsRelation.objects.create(user=personName, image=relevantPic, event=event_)


        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    # Guest mode
    elif mode == "guest":
        profilePic = None
        print(profilePic)
        if userr:  # If a valid user object exists
            profilePic = userr.profilepicture

        if not profilePic:  # If profilePic is not provided
            if request.method == "POST":
                profilePic = request.FILES['uploadedPhoto']
                print(profilePic)
        if profilePic:
            for pic in pics:
                image_path = os.path.join(settings.MEDIA_ROOT, str(pic.image))
                result = cropOut(image_path, profilePic)
                if result:
                    relevantPic = PicsRelation.objects.get(image=str(pic.image).replace('\\', '/'))
                    relevant_pics.append(image_path)

            if relevant_pics:
                # Create a zip file for download
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                    for file_path in relevant_pics:
                        zip_file.write(file_path, os.path.basename(file_path))
                zip_buffer.seek(0)

                response = HttpResponse(zip_buffer, content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="YourPics.zip"'
                return response

    return redirect("/")








    

@login_required
def addPhotos(request, eventID):
    if request.method == "POST":
        event = Event.objects.get(id=eventID)
        eventPics = request.FILES.getlist('file')  # Change the key to 'file' to match Dropzone
       # Save multiple event pictures in the PicsRelation model
        for file in eventPics:
            PicsRelation.objects.create(event=event, image=file)
            print(f"Picture saved for event: {event.name}")
    return redirect("/myEvents/"+eventID)

@login_required
def eventPage(request, eventID):
    event = Event.objects.get(id=eventID)
    pictures = PicsRelation.objects.filter(event=event)
    thread = threading.Thread(target=checkSimilarImages, args=(request.user, eventID))
    thread.start()
    return render(request, 'eventPage.html',{'event':event, 'photos':pictures})


def eventsAsAGuest(request, userID):
    user = User.objects.get(id=userID)
    events = Event.objects.filter(guest=user)
    if request.user.is_authenticated:
        arrPics = []
        for event in events:
            try:
                arrPics.append(PicsRelation.objects.filter(event=event)[0])
            except:
                pass
    return render(request, "events.html", {"events":events, 'status':'guest', 'pics':arrPics})

@login_required
def myPhotos(request):
    if request.user.is_authenticated:
        picsUser = userPicsRelation.objects.filter(user=request.user)
        events = Event.objects.filter(guest=request.user)
        # picsEvent = PicsRelation.objects.filter(event__in=events)

        myBigArr = []
        for event in events:
            myArr = []
            for picUser in picsUser:
                pic = PicsRelation.objects.filter(event=event)
                if picUser.image in pic:
                    myArr.append(picUser)
            myBigArr.append([event, myArr])
        print(myBigArr[0][0])
        return render(request, 'myPhotos.html', {'myBigArr':myBigArr})

    else:
        return redirect("/")
    

@login_required
def publishEvent(request, eventID):
    event = Event.objects.get(id=eventID)
    if request.user.id == event.host.id:
        event.published = True
        event.save()
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status":"unauthorized"})

def checkEventStatus(request, eventID):
    event = Event.objects.get(id=eventID)
    return JsonResponse({"status":event.published})


def restrictEvent(request, eventID):
    event = Event.objects.get(id=eventID)
    event.published = False
    event.save()
    return JsonResponse({"status":"success"})


def PeopleInEvent(request, eventID):
    event = Event.objects.get(id=eventID)
    relations = AnonymousUserPicsRelation.objects.filter(event=event)
    people = []
    for relation in relations:
        people.append(relation.user)
    people = set(people)
    people = list(people)
    context = {"event":event, "people":people}
    return render(request,"PeopleInEvent.html", context)

@login_required
def personPhotos(request, eventID, personName):
    event = Event.objects.get(id=eventID)
    relations = AnonymousUserPicsRelation.objects.filter(event=event, user=personName)

    return render(request,"personPhotos.html", {"relations":relations, "event":event})
 