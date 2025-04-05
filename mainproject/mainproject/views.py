from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User 
from django.contrib import messages
from myapp.models import * 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import *


def home(request):
    return render(request,"index.html")

def events(request):
    return render(request,"events.html")

@login_required
def notes(request):
    return render(request,"notes.html")

def courses(request):
    return render(request,"courses.html")

@login_required
def profile(request):
    if request.user.is_superuser:
        standard = request.POST.get('std')
        if standard in (str(0),None):
            profile = Students.objects.all().order_by('-std')

        else:
            print(request.user)

            standard = int(standard)
            profile = Students.objects.filter(std = standard)
        return render (request,"admin.html",{'profile':profile})

    else:
        print(request.user.username)
        profile = Students.objects.filter(username=request.user.username)
        return render (request,"studentProfile.html",{'profile':profile})

def logOutView(request):
    logout(request)
    return redirect('/loginPage/')


def signupPage(request):
    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        studentName = data.get("name")
        mob = data.get("mob")
        std = data.get("std")
        password = data.get("password")
        # print(data)
        if (User.objects.filter(username=username).exists()):
            messages.error(request,"User with same username already exists use different username")
            return redirect('/signupPage/')
        user = User.objects.create(
            username = username,
            first_name = studentName,
        ) 
        user.set_password(password)
        user.save()

        student = Students.objects.create(
            user = user,
            username = username,
            studentName = studentName,
            std = int(std),
            mob = mob,  
        )
        student.save()
        messages.info(request,"Account created successfully ")
        return redirect ('/signupPage/')
    return render (request,"signupPage.html")




def loginPage(request):
    if request.method == "POST":
        data = request.POST
        username=data.get("username")
        password=data.get("password")

        if not (User.objects.filter(username=username).exists()):
            messages.error(request,"Username not valid")
            return redirect('/loginPage/')
        user = authenticate(username=username,password=password)

        if user is None:
            messages.error(request,'invalid Password')
            return redirect('/login/')

        else:
            login(request,user)
            return redirect('/profile/')        
    return render(request,"loginPage.html")