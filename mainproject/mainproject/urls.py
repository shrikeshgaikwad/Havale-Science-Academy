"""
URL configuration for mainproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainproject.views import *
from myapp.views import * 
from messageModule.views import * 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name="home"),

    path('notes/',notes,name="notes"),
    path('manageNotes/',manageNotes,name="manageNotes"),
    path('deleteNotes/<int:notesId>/',deleteNotes,name="deleteNotes"),

    path('events/',eventGallery,name="events"),
    path('manageEvents/',manageEvents,name="manageEvents"),
    path('deleteEvent/<int:eventId>/',deleteEvent,name="deleteEvent"),
    
    path('loginPage/',loginPage,name="loginPage"),
    path('signupPage/',signupPage,name="signup Page"),
    path('profile/',profile,name="student profile page"),
    path('logout/',logOutView,name="Logout "),
    
    path('updateFeesTable/',updateFeesTable,name="updateFeesTable"),
    path('updateMarks/',updateMarks,name="updateMarks"),
    path('updateAttendanceTable/',updateAttendanceTable,name="updateAttendanceTable"),

    path('teachersData/',teachersData,name="teachersData"),




]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
