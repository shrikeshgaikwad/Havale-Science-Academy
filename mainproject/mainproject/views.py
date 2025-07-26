from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User 
from django.contrib import messages
from myapp.models import * 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import *
from mainproject.forms import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import os 
from django.conf import settings


def home(request):
    return render(request,"index.html")



@login_required
def profile(request):
    if request.user.is_superuser:
        fees = Fees.objects.all()
        marks = Marks.objects.all()
        attendance = Attendance.objects.all()
        students = Students.objects.all()
        
        if request.method == "POST":
            searchCategoty =request.POST.get("searchCategory")

            if searchCategoty=="std":
                try:
                    standard = request.POST.get("detail")
                    if standard in (str(0),None):
                        students = Students.objects.all().order_by('-std')

                    else:

                        standard = int(standard)
                        students = Students.objects.filter(std = standard)
                except ValueError:
                    messages.error(request,"Standard should be between 1 and 10, Enter 0 if you want to see the data of all students.")
                    
            if searchCategoty== "username":
                try:
                    username = request.POST.get("detail")
                    if username == None:
                        students = Students.objects.all().order_by('-std')

                    elif Students.objects.filter(username=username).exists():
                        username = str(username)
                        students = Students.objects.filter(username = username)

                    else :
                        students = Students.objects.all()
                        messages.error(request,"Specified Username does not Exist.")
                except ValueError:
                    messages.error(request,"Specified Username does not Exist.")
                

            if searchCategoty== "name":
                try:
                    name = request.POST.get("detail")
                    name = str(name)
                    if name == None:
                        students = Students.objects.all().order_by('-std')

                    elif Students.objects.filter(studentName=name).exists():
                        students = Students.objects.filter(studentName = name)

                    else :
                        students = Students.objects.all()
                        messages.error(request,"No student with specified name exists, Please check.")
                except ValueError:
                    messages.error(request,"Student name not valid.")


            if searchCategoty== "mob":
                try:
                    mob = request.POST.get("detail")
                    mob = int(mob)
                    if mob == None:
                        students = Students.objects.all().order_by('-std')

                    elif Students.objects.filter(mob=mob).exists():
                        students = Students.objects.filter(mob = mob)

                    else :
                        students = Students.objects.all()
                        messages.error(request,"Mobile number does not exists.")
                except ValueError:
                    messages.error(request,"Mobile number not valid.")

            if searchCategoty== "subject":
                try:
                    subject = request.POST.get("detail")
                    subject = str(subject)
                    if subject == None:
                        students = Students.objects.all().order_by('-std')
                        marks = Marks.objects.all()

                    elif Marks.objects.filter(subject=subject).exists():
                        marks = Marks.objects.filter(subject=subject)
                        
                    else :
                        students = Students.objects.all()
                        messages.error(request,"Subject doesn't Exist.")
                except ValueError:
                    messages.error(request,"Subject name not valid.")
        return render (request,"admin.html",{'students':students,'marks':marks,'fees':fees,'attendances':attendance})

    else:
        print(request.user.username)
        students  = Students.objects.filter(username=request.user.username)
        marks  = Marks.objects.filter(username=request.user.username)
        attendance  = Attendance.objects.filter(username=request.user.username)
        fees  = Fees.objects.filter(username=request.user.username)
        return render (request,"studentProfile.html",{'students':students,'marks':marks,'fees':fees,'attendances':attendance})

def logOutView(request):
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
def updateFeesTable(request):
    if request.user.is_superuser:
        fees = Fees.objects.all()
        standard = request.POST.get('std')
        if standard in (str(0),None):
            students = Students.objects.all().order_by('-std')

        else:
            print(request.user)

            standard = int(standard)
            profile = Students.objects.filter(std = standard)


    if request.method == "POST" :
        data = json.loads(request.body)
        updated_data = data.get('data', [])
        # print(updated_data)

        for row in updated_data:
            print(updated_data)
            username = row.get('column_0')
            name = row.get('column_1')
            newstd = row.get('column_2')
            mobile = row.get('column_3')
            fees = row.get('column_4')
            due = row.get('column_5')
            try:
                student = Students.objects.get(username=username)

                student.studentName = name
                student.std = newstd
                student.mob = mobile
                student.totalFees = fees
                student.dueFees = due
                student.save()
            except Students.DoesNotExist:
                messages.error(request,f"Student with username '{username}' not found.")

        return JsonResponse({'success': True})
    
    return render (request,"updateFees.html",{'students':students,'fees':fees})
    




@csrf_exempt
def updateMarks(request):
    if request.user.is_superuser:
        marks = Marks.objects.all()
        standard = request.POST.get('std')
        
        if standard in (str(0),None):
            students = Students.objects.all().order_by('-std')

        else:
            print(request.user)

            standard = int(standard)
            profile = Students.objects.filter(std = standard)


    if request.method == "POST" :
        data = json.loads(request.body)
        updated_data = data.get('data', [])
        # print(updated_data)

        for row in updated_data:
            print(updated_data)
            username = row.get('column_0')
            name = row.get('column_1')
            newstd = row.get('column_2')
            subject = row.get('column_3')
            totalMarks = row.get('column_4')
            score = row.get('column_5')
            percentage = row.get('column_6')
            try:
                if(totalMarks==None):
                    totalMarks = 0
                if(score==None):
                    score = 0
                if percentage == None:
                    percentage = 0
                marks = Marks.objects.get(username=username)
                student = Students.objects.get(username=username)
                student.studentName = name
                student.std = newstd
                marks.subject = subject
                marks.totalMarks = totalMarks
                marks.scoredMarks = score
                marks.percentage = percentage
                marks.save()
                student.save()
            except Students.DoesNotExist:
                messages.error(request,f"Student with username '{username}' not found.")

        return JsonResponse({'success': True})
    
    return render (request,"updateMarks.html",{'students':students,'marks':marks})
    



@csrf_exempt
def updateAttendanceTable(request):
    if request.user.is_superuser:
        attendance = Attendance.objects.all()
        standard = request.POST.get('std')
        if standard in (str(0),None):
            students = Students.objects.all().order_by('-std')

        else:
            print(request.user)

            standard = int(standard)
            profile = Students.objects.filter(std = standard)


    if request.method == "POST" :
        data = json.loads(request.body)
        updated_data = data.get('data', [])

        for row in updated_data:
            print(updated_data)
            username = row.get('column_0')
            name = row.get('column_1')
            newstd = row.get('column_2')
            presentDays = row.get('column_3')
            absentDays = row.get('column_4')

            try:
                student = Students.objects.get(username=username)
                attendance = Attendance.objects.get(username=username)
                student.studentName = name
                student.std = newstd
                attendance.presentDays =  presentDays
                attendance.absentDays = absentDays
                student.save()
                attendance.save()
            except Students.DoesNotExist:
                messages.error(request,f"Student with username '{username}' not found.")

        return JsonResponse({'success': True})
    
    return render (request,"updateAttendance.html",{'students':students,'attendances':attendance})
    
