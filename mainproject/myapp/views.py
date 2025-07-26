import os 
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User 
from myapp.models import * 
from django.contrib.auth.decorators import *
from mainproject.forms import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings





# Events
def eventGallery(request):
    events = Events.objects.all().order_by('-year')
    return render(request,"events.html",{'events':events})

@login_required
def manageEvents(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
            return redirect('manageEvents')
            
        else:
            events = Events.objects.all().order_by('-year')
            form = EventForm()
            return render(request,"addEvent.html",{'events':events,'form':form})


@login_required
def deleteEvent(request,eventId):
    event = get_object_or_404(Events,id=eventId)

    if event.image :
        image_path = os.path.join(settings.MEDIA_ROOT,str(event.image))
        if os.path.exists(image_path):
            os.remove(image_path)
            event.delete()
    return redirect("manageEvents")





# Notes
@login_required
def notes(request):
    return render(request,"notes.html")

@login_required
def manageNotes(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = NotesForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
            return redirect("manageNotes")

        else:
            notes = Notes.objects.all().order_by("-std")
            form = NotesForm()
            return render(request,"manageNotes.html",{'notes':notes,'form':form})

    return render(request,"manageNotes.html")

@login_required
def deleteNotes(request,notesId):
    notes = get_object_or_404(Notes,id=notesId)

    if notes.notesFile:
        notesPath = os.path.join(settings.MEDIA_ROOT,str(notes.notesFile))
        if os.path.exists(notesPath):
            os.remove(notesPath)
            notes.delete()
    return redirect("manageNotes")



@login_required
def teachersData(request):
    return render(request,"teachersData.html")