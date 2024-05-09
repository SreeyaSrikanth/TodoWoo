from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CreateTodoForm
from .models import Todo


def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signup.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signup.html', {'form':UserCreationForm(), 'error':'That username already exists'})
        else:
            return render(request, 'todo/signup.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login.html', {'form':AuthenticationForm(), 'error':'Username or Password is incorrect'})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/create.html', {'form':CreateTodoForm()})
    else:
        try:
            newtodo = CreateTodoForm(request.POST).save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/create.html', {'form':CreateTodoForm(), 'error':'Data imput is not valid. Try again'})

@login_required    
def currenttodos(request):
    now = timezone.now()
    todos = Todo.objects.filter(user=request.user,is_complete=False)
    todoscomp = Todo.objects.filter(user=request.user,is_complete=True).order_by('-complete_time')
    return render(request, 'todo/current.html', {'todos':todos, 'todoscomp':todoscomp, 'now':now})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = CreateTodoForm(instance=todo)
        return render(request, 'todo/view.html', {'todo':todo, 'form':form})
    else:
        try:
            form = CreateTodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/view.html', {'todo':todo, 'form':form, 'error':'Data input is not valid. Try again'})

@login_required      
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.complete_time = timezone.now()
        todo.is_complete = True
        todo.save()
        return redirect('currenttodos')

@login_required
def incompletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.complete_time = None
        todo.is_complete = False
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')