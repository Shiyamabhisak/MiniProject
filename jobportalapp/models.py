from django.db import models

# Create your models here.

class User_account(models.Model):
    name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    phone_no = models.BigIntegerField()
    mail_id = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    date = models.DateTimeField()
        
class Jobs(models.Model): 
    jobcode = models.CharField(max_length=100)  
    companyname = models.CharField(max_length=100)
    jobrole = models.CharField(max_length=100)
    dateposted = models.DateField(auto_now=False, auto_now_add=False)
    endingdate = models.DateField(auto_now=False, auto_now_add=False)
    jobdescription = models.FileField(upload_to="media/")
    appliedcandidates = models.PositiveIntegerField()
    visibility = models.BooleanField(default=False)
    location = models.CharField(max_length=100)
    experience = models.SmallIntegerField()
    salary = models.IntegerField()
    userid = models.ForeignKey(User_account,on_delete=models.CASCADE)
    
        
class AppliedCandidates(models.Model):
    name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    phone_no = models.BigIntegerField()
    mail_id = models.CharField(max_length=100)
    jobcode = models.CharField(max_length=100)
    resume = models.FileField(upload_to="resumeMedia/")
    matching = models.FloatField()
    age = models.IntegerField()
    skills = models.CharField(max_length=100)
    experience = models.IntegerField()
    userid = models.ForeignKey(User_account,on_delete=models.CASCADE)
    