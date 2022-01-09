"""miniproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from jobportalapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.indexpage),
    path('userindex/',views.userindexpage),
    path('userlogin/',views.loginpage),
    path('user-registration/',views.registrationpage),
    path('candidate/',views.candidate),
    path('recruiter/',views.recruiter),
    path('upload/',views.upload),
    path('register/',views.userregistration),
    path('login/',views.userlogin),
    path('userprofile/',views.userprofile),
    path('logout',views.signout),
    path('filematch/',views.filematch),
    path('viewcandidates/',views.viewcandidates),
    path('delete/',views.delete),
    path('edit/',views.edit),
    path('editedprofile/',views.editedprofile),
    path('viewdetailedprofile/',views.viewdetailedprofile),
    path('jobcodefilter/',views.filterjobcode),
    path('filter/',views.filter),
    path('candiddetails/',views.candiddetails),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
