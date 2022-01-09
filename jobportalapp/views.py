from django.core.checks import messages
from django.http import response,HttpResponse
from django.shortcuts import redirect, render
from numpy.lib.function_base import percentile
from django.core.cache import caches
from jobportalapp.models import AppliedCandidates, Jobs,User_account
from miniproject.settings import BASE_DIR, MEDIA_ROOT
import datetime
import random
import docx2txt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib import messages
import os
import math

# Create your views here.
def indexpage(request):
    return render(request,'jobportalapp/index.html')

def userindexpage(request):
    return render(request,'jobportalapp/user-index.html')

def loginpage(request):
    return render(request,'jobportalapp/Login.html')

def registrationpage(request):
    return render(request,'jobportalapp/Registration.html')

def candiddetails(request):
    jobcode = request.POST['jobcode']
    response = render(request,'jobportalapp/candidateform.html')
    response.set_cookie('jobcode',jobcode)
    return response
    
def recruiter(request):
    userid = request.COOKIES.get('userid')
    res = Jobs.objects.filter(userid=userid)
    return render(request,'jobportalapp/Recruiter.html',{'res' : res})

def candidate(request):
    return render(request,'jobportalapp/filter.html')

def upload(request):
    jobrole = request.POST['jobrole']
    companyname = request.POST['companyname']
    startingdate = datetime.datetime.now()
    endingdate = request.POST['endingdate']
    jobcode = companyname[0:3] + str(random.randrange(100, 1000, 3))
    file = request.FILES['file']
    
    visibility = request.POST.get('visibility')
    if visibility is None:
        visibility = False
    else :
        visibility = True
    location = request.POST['location']
    experience = request.POST.get('exp')
    salary = request.POST['salary']
    userid = request.COOKIES.get('userid')
    obj = User_account.objects.get(id=userid)
    jobs = Jobs(jobcode=jobcode,jobrole=jobrole,companyname=companyname,dateposted=startingdate,endingdate=endingdate,jobdescription=file,appliedcandidates=0,visibility=visibility,location=location,experience=experience,salary=salary,userid=obj)
    jobs.save()
    return recruiter(request)

def userregistration(request):
    name = request.POST['name']
    username = request.POST['username']
    phone = request.POST['phoneno']
    mailid = request.POST['mailid']
    password = request.POST['password']
    confirm_password = request.POST['password2']
    if password == confirm_password:
        if User_account.objects.filter(user_name=username).exists():
            messages.info(request,'Username taken')
            return redirect('/user-registration')
        elif  User_account.objects.filter(mail_id=mailid).exists():
            messages.info(request,'Mail - ID already in use')
            return redirect('/user-registration')
        else:    
            user = User_account(name=name,user_name=username,phone_no=phone,mail_id=mailid,password=password,date=datetime.datetime.now())
            user.save()
    else:
        messages.info(request,'Password not matching')
        return redirect('/user-registration')
    
    return render(request,'jobportalapp/Login.html')

def userlogin(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        user = User_account.objects.get(user_name=username)
    except User_account.DoesNotExist:
        user = None
    if user is not None:
        if user.password==password:
            response = render(request,'jobportalapp/user-index.html',{'user' : user})
            response.set_cookie('userid',user.id)
            return response
        else:
            messages.info(request,'Password is incorrect')
            return redirect('/userlogin')
    else:
        messages.info(request,'User not found ... Plz register')
        return redirect('/userlogin')

def userprofile(request):
    userid = request.COOKIES.get('userid')
    if userid is None:
        try:
            userid = request.COOKIES['userid']
        except Exception as e:
            raise e
    
    userobj = User_account.objects.get(id=userid)
    return render(request,'jobportalapp/profile.html',{'user' : userobj})

def filematch(request):
    age = request.POST['age']
    skills = request.POST['skills']
    exp = request.POST['exp']
    diff = int(age) - int(exp)
    if diff < 21:
        messages.info(request,'Your Experience doesnt match the requirements')
        return redirect('/candidate')
    file = request.FILES['resume']
    resume = docx2txt.process(file)
    
    jobcode = request.COOKIES.get('jobcode')
    obj = Jobs.objects.get(jobcode=jobcode)
    if int(exp) < int(obj.experience) :
        messages.info(request,'Your Experience doesnt match the requirements')
        return redirect('/candidate')
    
    userid = request.COOKIES.get('userid')
    userObj = User_account.objects.get(id=userid)
    name = userObj.name
    username = userObj.user_name
    phone = userObj.phone_no
    mail = userObj.mail_id

    description = docx2txt.process(os.path.join(BASE_DIR,MEDIA_ROOT,obj.jobdescription.name))
    
    text = [resume,description]

    cv = CountVectorizer()

    count_matrix = cv.fit_transform(text)

    matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
    matchPercentage = round(matchPercentage,2)

    candidate = AppliedCandidates(name=name,user_name=username,phone_no=phone,mail_id=mail,jobcode=jobcode,resume=file,matching=matchPercentage,age=age,skills=skills,experience=exp,userid=userObj)
    
    
    print("Your Resume matches about " +str(matchPercentage) + "% of the Job Description")
    if matchPercentage > 30:
        candidate.save()
        obj.appliedcandidates += 1
        obj.save()
        return render(request,'jobportalapp/appliedsuccess.html')
    else:
        return redirect('/candidate')
    

def viewcandidates(request):
    jobcode = request.POST['jobcode']
    res = AppliedCandidates.objects.filter(jobcode=jobcode).order_by('matching')
    return render(request,'jobportalapp/appliedcandidates.html',{'res' : res})

def viewdetailedprofile(request):
    jobcode = request.POST['jobcode']
    username = request.POST['username']
    res = AppliedCandidates.objects.filter(jobcode=jobcode,user_name=username).last()
    res.matching = int(res.matching)
    return render(request,'jobportalapp/viewfulldetails.html',{'res' : res})

def delete(request):
    jobcode = request.GET['jobcode']
    obj = Jobs.objects.get(jobcode=jobcode)
    obj.delete()
    userid = request.COOKIES.get('userid')
    res = Jobs.objects.filter(personid=userid)
    return render(request,'jobportalapp/recruiter.html' ,{'res' : res})

def edit(request):
    userid = request.COOKIES.get('userid')
    if userid is None:
        try:
            userid = request.COOKIES['userid']
        except Exception as e:
            raise e
    
    userobj = User_account.objects.get(id=userid)
    return render(request,'jobportalapp/editprofile.html',{'user' : userobj})

def editedprofile(request):
    userid = request.COOKIES.get('userid')
    if userid is None:
        try:
            userid = request.COOKIES['userid']
        except Exception as e:
            raise e
    name = request.POST['name']
    username = request.POST['username']
    phone = request.POST['phoneno']
    mailid = request.POST['mailid']
    password = request.POST['password']
    userobj = User_account.objects.get(id=userid)
    userobj.name = name
    userobj.user_name = username
    userobj.phone_no = phone
    userobj.mail_id = mailid
    userobj.password = password
    userobj.save()
    return render(request,'jobportalapp/profile.html',{'user' : userobj})

def filterjobcode(request):
    jobcode = request.POST['jobcode']
    res = Jobs.objects.filter(jobcode=jobcode)
    return render(request,'jobportalapp/candidate.html',{'res' : res})

def filter(request):
    companyname = request.POST['companyname']
    jobname = request.POST['jobname']
    salary = request.POST['salary']
    experience = request.POST['experience']
    userid = request.COOKIES.get('userid')
    appliedjobs = AppliedCandidates.objects.filter(userid=userid)
    obj = Jobs.objects.filter(visibility=0)
    obj.exclude(jobcode__in=list(appliedjobs))
            
    if companyname and not companyname.isspace():
        obj = obj.filter(companyname=companyname)
        
    if jobname and not jobname.isspace():
        obj = obj.filter(jobrole=jobname)
        
    if salary and not salary.isspace():
        obj = obj.filter(salary__gte = salary)
        
    if experience and not experience.isspace():
        obj = obj.filter(experience__gte = experience)
           
    return render(request,'jobportalapp/candidate.html',{'res' : obj})

def signout(request):
    return render(request,'jobportalapp/index.html')
    