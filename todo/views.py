from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

def home(request):
    return render(request,'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
         return render(request,'todo/signupuser.html',{'form':UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2'] :
            try:
                user =User.objects.create_user(
                    request.POST['username'],
                    request.POST['password1'],
                    request.POST['password2'])
                user.save()
                login(request, user)
                return redirect(currenttodos)
            except IntegrityError:
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error' :'the user already exist'})
        else:
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error' :'passwords do not match'})

def loginuser(request):
    if request.method == 'GET':
         return render(request,'todo/loginuser.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request, username= request.POST['username'],password= request.POST['password'])
        if user is None:
            return  render(request,'todo/loginuser.html',{'form':AuthenticationForm(),'error':'invalid user/password'})
        else:
            login(request, user)
            return redirect(currenttodos)


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        print('return redirect(home)')
        return redirect('home')


def currenttodos(request):
    return render(request,'todo/currenttodos.html')
