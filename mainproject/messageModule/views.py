import os
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from myapp.models import *
from messageModule.models import * 
from django.contrib.auth.decorators import * 
from mainproject.forms import * 
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings



# @login_required
# def chat(request,username):
#     receiverUser = User.objects.get(username=username)
#     messages = customMessages.objects.filter(
#         sender = request.user,
#         receiver = receiverUser
#     ) | customMessages.objects.filter(
#         sender = receiverUser,
#         receiver = request.user
#     )


#     messages = messages.order_by("timeStamp")


#     if request.method == 'POST':
#         content = request.POST.get('message')
#         if content:
#             customMessages.objects.create(sender=request.user, receiver=receiverUser, content=content)
#             return redirect('chat', username=receiverUser.username)

#     return render(request, 'chat.html', {
#         'messages': messages,
#         'receiverUser': receiverUser
#     })
