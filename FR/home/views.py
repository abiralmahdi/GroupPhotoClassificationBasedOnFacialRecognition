from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, PicsRelation
from django.contrib.auth.models import User

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

def myEvents(request):
    if request.user.is_authenticated:
        events = Event.objects.filter(host=request.user)
        return render(request, 'events.html', {'events': events})
    else:
        return redirect("/")
    

def addEvents(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        guest_ids = request.POST.getlist('guests')  # Get guest IDs as a list
        event_date = request.POST.get('event_date')
        eventPic = request.FILES.get('eventPic')
        host = request.user

        # Create the Event instance
        event = Event(name=name, description=description, event_date=event_date, host=host, eventPic=eventPic)
        event.save()

        # Fetch the User objects corresponding to the guest IDs
        guests = User.objects.filter(id__in=guest_ids)

        # Set the guests for the many-to-many relationship
        event.guest.set(guests)

        for file in eventPic:
            PicsRelation.objects.create(event=event, image=file)
        event.save()

        return redirect("/myEvents")
    
    return redirect("/")