from django.db import models
from django.contrib.auth.models import User
from myapp.models import * 


# class customMessages(models.Model):
#     sender = models.ForeignKey(User,related_name="sentMessage",on_delete=models.CASCADE)
#     receiver = models.ForeignKey(User,related_name="receivedMessage",on_delete=models.CASCADE)
#     content = models.TextField()
#     timeStamp = models.DateTimeField(auto_now_add=True)


#     class Meta:
#         ordering = ['timestamp']

#     def __str__(self):
#         return f'{self.sender.username} -> {self.receiver.username}: {self.content[:]}'
