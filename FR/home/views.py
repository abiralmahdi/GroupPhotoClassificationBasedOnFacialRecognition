from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Event, PicsRelation
from django.db import transaction
from django.contrib import messages


User = get_user_model()  # Correctly get the User model

@login_required
def index(request):
    users = User.objects.all()  # Removed the instantiation
    return render(request, 'index.html', {'users': users})

def myEvents(request):
    if request.user.is_authenticated:
        users = User.objects.all()  # Removed the instantiation
        events = Event.objects.filter(host=request.user)
        return render(request, 'events.html', {'events': events, 'users': users})
    else:
        return redirect("/")

def addEvents(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
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

                # Handle the uploaded pictures
                eventPics = request.FILES.getlist('file')  # Change the key to 'file' to match Dropzone

                # Save multiple event pictures in the PicsRelation model
                for file in eventPics:
                    PicsRelation.objects.create(event=event, image=file)

            return redirect("/myEvents")

        except Exception as e:
            print(f"Error: {e}")  # Log the error for debugging purposes
            messages.error(request, "There was an error while creating the event. Please try again.")

            # Redirect to the same page to allow the user to fix the error
            return redirect("/")

    # If it's not a POST request, redirect to the home page
    return redirect("/")
