from django.db import models
from django.contrib.auth.models import User

 
class Students(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    studentName = models.CharField(max_length=25)
    username = models.CharField(max_length=20)
    mob = models.CharField(max_length=10)
    std = models.IntegerField(max_length=2)



class Fees(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    totalFees = models.IntegerField(max_length=10,null=True,blank=True,default=0)
    paidFees = models.IntegerField(max_length=10,null=True,blank=True,default=0)
    dueFees = models.IntegerField(max_length=10,null=True,blank=True,default=0)


class Marks(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    testDate = models.DateField(null=True,blank=True)
    subject = models.CharField(max_length=15,null=True,blank=True)
    totalMarks = models.IntegerField(max_length=4,null=True,blank=True)
    scoredMarks = models.IntegerField(max_length=4,null=True,blank=True)
    percentage = models.IntegerField(max_length=4,null=True,blank=True)



class Events(models.Model):
    image = models.ImageField(upload_to='')
    year =  models.IntegerField(max_length=4,null=True,blank=True)
    description = models.CharField(max_length=255)


class Notes(models.Model):
    std = models.IntegerField(max_length=3,null=True,blank=True)
    subject = models.CharField(max_length=20,null = True, blank= True)
    chaptername = models.CharField(max_length=20,null = True, blank= True)
    notesFile = models.FileField(upload_to='notes/')
    url = models.URLField()


class Attendance(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    presentDays = models.IntegerField(max_length=5,null=True,blank=True)
    absentDays = models.IntegerField(max_length=5,null=True,blank= True)

class defaultFees(models.Model):
    std = models.IntegerField(max_length=2,null=False,blank=False)
    defaultFees = models.IntegerField(max_length=5,null=True,blank=True)