from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User 
from django.contrib import messages
from myapp.models import * 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import *
from mainproject.forms import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def home(request):
    return render(request,"index.html")




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
                return redirect('manageEvent')
        else:
            events = Events.objects.all().order_by('-year')
            return render(request,"addEvent.html",{'evnets':events})

    

@login_required
def notes(request):
    return render(request,"notes.html")



def courses(request):
    return render(request,"courses.html")



@login_required
def profile(request):
    if request.user.is_superuser:
        fees = Fees.objects.all()
        marks = Marks.objects.all()
        attendance = Attendance.objects.all()
        standard = request.POST.get('std')
        if standard in (str(0),None):
            students = Students.objects.all().order_by('-std')

        else:
            print(request.user)

            standard = int(standard)
            profile = Students.objects.filter(std = standard)
        return render (request,"admin.html",{'students':students,'marks':marks,'fees':fees,'attendances':attendance})

    else:
        print(request.user.username)
        students  = Students.objects.filter(username=request.user.username)
        marks  = Marks.objects.filter(username=request.user.username)
        attendance  = Attendance.objects.filter(username=request.user.username)
        fees  = Fees.objects.filter(username=request.user.username)
        return render (request,"studentProfile.html",{'students':students,'marks':marks,'fees':fees,'attendances':attendance})



def logOutView(request):
    print("logout")
    logout(request)
    return redirect('loginPage')


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
        fees = Fees.objects.create(
            user = user,
            username = username,
            
        )
        fees.save()

        marks = Marks.objects.create(
            user = user,
            username = username,

        ) 
        marks.save()

        attendance = Attendance.objects.create(
            user  = user,
            username = username,
        )
        attendance.save()
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
            messages.error(request,"Invalid Password")
            return redirect('/loginPage/')

        else:
            login(request,user)
            return redirect('/profile/')        
    return render(request,"loginPage.html")







@csrf_exempt
def updateDatabase(request):

    if request.method == "POST" :
        data = json.loads(request.body)
        updated_data = data.get('data', [])
        # print(updated_data)

        for row in updated_data:
            
            username = row.get('column_0')
            name = row.get('column_1')
            newstd = row.get('column_2')
            mobile = row.get('column_3')
            fees = row.get('column_4')
            due = row.get('column_5')
            try:
                student = Students.objects.get(username=username)
                # print(student.std)
                # print(newstd)
                # print(student.std)
                # print(newstd)
                student.studentName = name
                student.std = newstd
                student.mob = mobile
                student.totalFees = fees
                student.dueFees = due
                student.save()
            except Students.DoesNotExist:
                print(f"Student with username '{username}' not found.")

        return JsonResponse({'success': True})

