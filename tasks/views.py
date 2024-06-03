from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
# Create your views here.
def home(request):
    return render(request, 'home.html')
def signup(request):
    
    if request.method == 'GET':
         return render(request,'signup.html',{
        'form': UserCreationForm
    })
    
    else:
        if request.POST['password1'] == request.POST['password2']:
            #register user
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], email=request.POST['email'])
                email1=request.POST['email']
                user.save()
                login(request, user)
                send_mail(
                'Hola desde django app',
                'Felicidades has creado tu cuenta exitosamente',
                'pruebadedjango46@gmail.com',
                [email1],
                fail_silently=False  
                )
                return redirect('tasks')
            except IntegrityError:
                return render(request,'signup.html',{
                'form': UserCreationForm,
                'error': 'El usuario ya existe'
                })
        return render(request,'signup.html',{
        'form': UserCreationForm,
        'error': 'Las contraseñas no coinciden'
        })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull=True)
    
    return render(request, 'tasks.html',{'tasks': tasks})

@login_required
def tasks_complete(request):
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull=False).order_by('-datecompleted')
    
    return render(request, 'tasks.html',{'tasks': tasks})

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signip(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
        'form': AuthenticationForm
    })
    else:
       user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
       
       if user is None:
           return render(request, 'signin.html',{
        'form': AuthenticationForm,
        'error': 'Usario o contraseña incorrectas'
        })
       else:
           login(request, user)
           return redirect('tasks')

@login_required       
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
        'form': TaskForm
    })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html',{
                'form': TaskForm,
                'error': 'Por favor valide la data'
            })

@login_required            
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render (request, 'task_detail.html', {
            'task':task,
            'form':form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST,instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render (request, 'task_detail.html', {
            'task':task,
            'form':form,
            'error': 'Error al actualizar el formulario'
        })

@login_required    
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user= request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required    
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user= request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.delete()
        return redirect('tasks')     

@login_required
def perfil(request, user_id):
    datos = User.objects.get(id=user_id)
    return render(request, 'profile.html',{
        'datos': datos
    })

@login_required
def editProfile(request, user_id):
        if request.method == 'GET':
            datos = User.objects.get(id=user_id)
            return render(request, 'edit_profile.html',{
            'datos': datos
        })
        else:
            user_id = request.POST['id']
            name = request.POST['userName']
            mail = request.POST['userEmail']
            
            datos = User.objects.get(id=user_id)
            datos.username = name
            datos.email = mail
            datos.save()
            return redirect('/')
        
def solicitarRestablecerContra(request, user_id):
        user = User.objects.get(id=user_id)
        token = default_token_generator(user)
        reset_url = request.build_absolute_uri(reverse('restablecer_contraseña', args=[token]))
        send_mail(
            'Restablecer tu contraseña',
            f'Por favor, haz clic en el siguiente enlace para restablecer tu contraseña: {reset_url}',
            'pruebadedjango46@gmail.com',
            [user.email],
            fail_silently=False
        )
        return redirect(request, 'restablecer_contraseña.html')
    
def restablecer_contraseña(request):
    return render(request, 'restablecer_contraseña.html')