from django.shortcuts import render
# Imports needed for registration
from basic_app.forms import UserForm,UserProfileInfoForm
from basic_app.models import UserProfileInfo
# Imports needed for login
from django.urls import reverse
from django.contrib.auth.decorators import login_required # For views manipulation that require users to be logged-in
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout


# Create your views here.

def index(request):
    return render(request, 'basic_app/index.html')

@login_required # Makes entire view availible only when user is logged-in
def user_logout(request):
    logout(request) # Automaticlly sends the request to logout by the user to the built-in logout function
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if(request.method == "POST"):
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if (user_form.is_valid() and profile_form.is_valid()):
            user = user_form.save() # Saves user data directly to database
            user.set_password(user.password) # To hash password
            user.save()
            profile = profile_form.save(commit=False) # To avoid collissions
            profile.user = user
            if('profile_pic' in request.FILES): # If user supplied a profile_pic, it's in request.FILES dict
                profile.profile_pic = request.FILES['profile_pic'] # Set the picture to user object profile_pic attr
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'basic_app/registration.html',{'user_form':user_form, 
                                                            'profile_form':profile_form, 
                                                            'registered':registered})

def user_login(request):
    if(request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password) # Authenticates user automaticlly thanks to django
        if(user):
            if(user.is_active):
                login(request, user) # After authenticating that user exists and is an active user log him in and send him to a webpage
                print("user authenticated")
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponseRedirect("Account not active")
        else:
            print("Someone tried to login and failed")
            print("User Name: {}, Password: {}\n".format(username,password))
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, 'basic_app/login.html', {})



