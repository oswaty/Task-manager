from django.shortcuts import render,redirect
from .models import Task
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django import forms
# Create your views here.

class NewTaskForm(forms.Form):
    title=forms.CharField(label="New Task")
    description=forms.CharField(label="Description")
    due_date=forms.DateField()


def index(request):
    return render(request,'tasks/index.html')



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasks:task_list')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tasks:task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('tasks:login')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form=NewTaskForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            description = form.cleaned_data['description']
            due_date=form.cleaned_data['due_date']
            task = Task.objects.create(title=title, description=description, due_date=due_date, user=request.user)
            return redirect('tasks:task_list')
        else:
             return render(request,"tasks/task_create.html",{
               "form":form 
            }) 
    return render(request, 'tasks/task_create.html',{
        "form":NewTaskForm()
    })

@login_required
def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    if task.user != request.user:
        raise Http404("You don't have permission to view this task.")
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_complete(request, pk):
    task = Task.objects.get(pk=pk)
    if task.user != request.user:
        raise Http404("You don't have permission to complete this task.")
    task.is_complete = True
    task.save()
    return redirect('task_list')


def task_incomplete(request, pk):
    task = Task.objects.get(pk=pk)
    if task.user!= request.user:
        raise Http404("You don't have permission to complete this task.")
    task.is_complete = False
    task.save()
    return redirect('task_list')