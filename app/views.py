from pickle import NONE
from django.shortcuts import render,redirect
from h11 import Response
from urllib3 import HTTPResponse
from app.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random
from django.shortcuts import get_object_or_404
# Create your views here.
def home(request):
    teachers_list = Teacher.objects.annotate(
        total_score=Sum(F('best') + F('average') + F('worst'))
    ).order_by('-total_score')
    context={
        'teacher':teachers_list,
    }
    return render(request,"home.html",context)


def login_page(request): 
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user_objects = User.objects.filter(username=username)
            if not user_objects.exists:
                messages.warning(request, "username does not exist")
                return redirect("login")
            user_objects = authenticate(username=username, password=password)
            if user_objects:
                login(request, user_objects)
                return redirect("/")
            messages.success(request, "wrong password")
            return redirect("login")
        except Exception as e:
            messages.error(request, "wrong credentials")
            return redirect(request, "register")

    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is taken.")
                return redirect("register")
            otp = random.randint(1000, 9999)
            send_email_to_user(username,otp)
            user_object = User.objects.create(username=username)
            user_object.set_password(password)
            messages.success(request, "User created successfully.")
            user_object.save()
            return render(request,"otp.html")
        except Exception as e:
            messages.error(request, "Something went wrong during registration.")

        return redirect("register")

    return render(request, "register.html")


from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view

def send_email_to_user(useremail,parameter):
    previous=CustomUser.objects.get(username=useremail)
    if previous is NONE:
        instance =CustomUser.objects.create(username=useremail,otp=parameter)
    parameter=previous.otp
    subject="OTP"
    message=f"{parameter}"
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[f"{useremail}"]
    send_mail(subject,message,from_email,recipient_list)
    
  
def otp_verify(request):
    if request.method=="POST":
        username=request.POST.get("username")
        otp=request.POST.get("otp")
        data = get_object_or_404(CustomUser, username=username, otp=otp)
        if data is not None:
            return redirect("rating")
        else:
            return HTTPResponse("wrong otp or username")
    else:
        return render(request,"otp.html")    
from django.db.models import F, Sum


@login_required 
@api_view(['GET','POST']) 
def rating(request):
    teachers_list = Teacher.objects.annotate(
        total_score=Sum(F('best') + F('average') + F('worst'))
    ).order_by('total_score')[:15]
    context={
        'teacher':teachers_list
    }
    
    if request.method=="POST":
        fulldata=request.POST
        dynamic_values = {key: value[0] for key, value in fulldata.items() if key != 'csrfmiddlewaretoken' and len(value) > 0}
        for name, value in dynamic_values.items():
            instance=Teacher.objects.get(name=name)
            if value=="0":
                instance.best=instance.best+1
            elif value=="1":
                instance.average=instance.average+1
            else:
                instance.worst=instance.worst+1
            instance.save()
    return render(request,"rating.html",context)