from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request,"index.html")

def events(request):
    return render(request,"events.html")

def notes(request):
    return render(request,"notes.html")

def loginPage(request):
    return render(request,"loginPage.html")



def courses(request):
    return render(request,"courses.html")

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")


def loginPage(request):
    return render(request,"loginPage.html")

def signupPage(request):
    return render (request,"signupPage.html")