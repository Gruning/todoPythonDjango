from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone

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

def createtodo(request):
    if request.method == 'GET':
        return render(request,'todo/createtodo.html',{'form':TodoForm})
    else:
        try:
            form = TodoForm(request.POST)
            #print(request.POST)
            newtodo = form.save(commit= False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request,'todo/createtodo.html',{'form':TodoForm(),'error':'bad data passed'})

def currenttodos(request):
    todos = Todo.objects.filter(
        user = request.user,
        dateCompleted__isnull=True
        ) 
    return render(request,'todo/currenttodos.html',{'todos':todos})

def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk= todo_pk, user = request.user)
    form = TodoForm(instance= todo)
    if request.method == 'GET':
        return render(request,'todo/viewtodo.html',{'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request,'todo/viewtodo.html',{'todo':todo,'form':form,'error':'Bad info'})

def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk= todo_pk, user = request.user)
    if request.method == 'POST':
        todo.dateCompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk= todo_pk, user = request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')