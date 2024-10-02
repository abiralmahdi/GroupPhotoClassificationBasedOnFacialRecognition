from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login,logout
from .models import *
from django.contrib.auth.hashers import make_password

def login(request):
    if request.method == "POST":
        data = request.POST
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect('/accounts/login/')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)  
            messages.success(request, "Successfully logged in")
            return redirect('')
        else:
            messages.error(request, "Invalid password")
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
        contact = data.get('contact')

        if checkvalidity(request,password,rpassword,Email):
            user = User.objects.create(username=Email, email=Email, first_name=Firstname, last_name=Lastname, password=make_password(password))
            user.contact = contact
            user.pwd = password
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('/accounts/login/')
        
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

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/accounts/login/')