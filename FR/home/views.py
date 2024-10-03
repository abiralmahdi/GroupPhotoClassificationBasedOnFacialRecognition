from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, PicsRelation
from django.contrib.auth import get_user_model as User


# Create your views here.
@login_required
def index(request):
    users = User().objects.all()
    return render(request, 'index.html', {'users':users})

def myEvents(request):
    if request.user.is_authenticated:
        users = User().objects.all()
        events = Event.objects.filter(host=request.user)
        return render(request, 'events.html', {'events': events, 'users':users})
    else:
        return redirect("/")
    

def addEvents(request):
    if request.method == "POST":
        name = request.POST.get('eventName')
        description = request.POST.get('eventDescription')
        guest_ids = request.POST.getlist('guests')  # Get guest IDs as a list
        event_date = request.POST.get('date')
        eventPics = request.FILES.getlist('file')  # Change the key to 'file' to match Dropzone
        host = request.user

        # Create the Event instance
        event = Event(name=name, description=description, event_date=event_date, host=host)
        event.save()

        # Fetch the User objects corresponding to the guest IDs
        guests = User().objects.filter(id__in=guest_ids)

        # Set the guests for the many-to-many relationship
        event.guest.set(guests)

        # Save multiple event pictures in the PicsRelation model
        for file in eventPics:
            PicsRelation.objects.create(event=event, image=file)
            print(f"Picture saved for event: {event.name}")

        return redirect("/myEvents")
    
    return redirect("/")
