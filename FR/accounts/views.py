from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from .models import *

def login(request):
    if request.method=="POST":
        data=request.POST
        Email=data.get('email')
        password=data.get('password')

        user=User.objects.filter(email=Email)

        if not user.exists() :
            messages.error(request,"User doesn't Exists")
            return redirect('/accounts/login/')
        
        else:
            user=User.objects.get(email=Email)
            username=user.username
            user=authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect('/chat/')
             
            else:
                messages.error(request,"Invalid Password")
                return redirect('/accounts/login/')
    return render(request, "login.html")




def register(request):
    if request.method=="POST":
        data=request.POST
        Firstname=data.get('first-name')
        Lastname=data.get('last-name')
        Email=data.get('email')
        password=data.get('password')
        rpassword=data.get('cpassword')

        if checkvalidity(request,password,rpassword,Email):
            username=f"{Firstname} {Lastname}"
            user = User.objects.create(username=username, email=Email, first_name=Firstname, last_name=Lastname)
            user.set_password(password) 
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('/home/')
        
    return render(request,"register.html")
    


def checkvalidity(request, passw, repeat_passw,Email):  #For checking Password validity during registration
    if len(passw) < 8:
        messages.error(request, "Passwords must be at least 8 characters")
        return False
    elif passw != repeat_passw:
        messages.error(request, "Passwords don't match")
        return False
    elif User.objects.filter(username=Email).exists():
        messages.error(request, "User Exists")
        return False
    
    return True
