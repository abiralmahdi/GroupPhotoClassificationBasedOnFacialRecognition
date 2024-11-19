from django.shortcuts import render, HttpResponse
from home.models import Event, PicsRelation

# Create your views here.

def sharedEvent(request, eventID):
    event = Event.objects.get(id=eventID)
    if not event.published:
        return HttpResponse("<h1>Restricted access</h1>")
    pictures = PicsRelation.objects.filter(event=event)
    return render(request, 'clienteventPage.html',{'event':event, 'photos':pictures,'eventcode':event.code})


   
