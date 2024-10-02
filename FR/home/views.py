from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Event

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