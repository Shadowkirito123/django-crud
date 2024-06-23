from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task, Tokens, Pagina, Colores
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from django.urls.exceptions import NoReverseMatch
from django.core.files.uploadedfile import SimpleUploadedFile
import re
import os
# Create your views here.
def home(request):
    form = Task.objects.all()
    return render(request, 'home.html',{
        'form': form
    })

def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html',{
        'form': UserCreationForm
    })
    
    else:
        if request.POST['password1'] == request.POST['password2']:
            username = request.POST['username']
            if re.search(r'[!@#$%^&*(),.?":{}|<>]', username):
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Los caracteres especiales no están permitidos.'
                })
            
            email = request.POST['email']
            if re.search(r'[!#$%^&*(),?":{}|<>]', email):
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Los caracteres especiales no están permitidos en el correo electrónico.'
                })
            
            first_name = request.POST['first_name']
            if re.search(r'[!@#$%^&*(),.?":{}|<>]', first_name):
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Los caracteres especiales no están permitidos en el nombre.'
                })
            
            last_name = request.POST['last_name']
            if re.search(r'[!@#$%^&*(),.?":{}|<>]', last_name):
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Los caracteres especiales no están permitidos en el apellido.'
                })
            
            elif User.objects.filter(username=username).exists():
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
            else:
                try:
                    user = User.objects.create_user(username=username, password=request.POST['password1'], email=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                    email1=request.POST['email']
                    username1 = request.POST['username']
                    user.save()
                    login(request, user)
                    send_mail(
                    'Hola desde django app',
                    'Felicidades has creado tu cuenta exitosamente',
                    'pruebadedjango46@gmail.com',
                    [email1],
                    fail_silently=False  
                    )
                    try:
                        #Captura de sitio web
                        
                        # Set up ChromeOptions
                        options = ChromeOptions()
                        options.add_argument("--headless")

                        # Create a new instance of the Chrome WebDriver
                        driver = webdriver.Chrome(options=options)

                        # Navigate to the webpage
                        webpage_url = request.POST['web']
                        driver.get(webpage_url)

                        # Take a screenshot of the webpage
                        screenshot_filename = f'C:/Users/Usuario/Documents/Cms/django-crud/static/{username1}.png'
                        driver.save_screenshot(screenshot_filename)

                        # Quit the WebDriver
                        driver.quit()

                        # Create a Django model instance
                        webpage_content = webpage_url
                        with open(screenshot_filename, 'rb') as f:
                            image_file = SimpleUploadedFile(f.name, f.read())
                        Pagina.objects.create(user=user, web=webpage_content, imagen=image_file)
                    except:
                        pass
                    #
                    
                    return redirect('/')
                except IntegrityError:
                    # Handle the IntegrityError here
                    pass
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
           return redirect('/')

@login_required       
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm(),
        })
    else:
        try:
            #Para subir tareas
            form = TaskForm(request.POST, request.FILES)
            if form.is_valid():
                new_task = form.save(commit=False)
                new_task.user = request.user
                new_task.save()
                return redirect('tasks')
            else:
                return render(request, 'create_task.html',{
                    'form': form,
                    'error': 'Por favor revise los errores en el formulario'
                })
        except ValueError:
            return render(request, 'create_task.html',{
                'form': TaskForm(),
                'error': 'Error interno, por favor intente de nuevo'
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
    try:
        datos = User.objects.get(id=user_id)
        datos1 = get_object_or_404(Pagina, user=user_id)
        return render(request, 'profile.html',{
            'datos': datos,
            'datos1': datos1
        })
    except:
        datos = User.objects.get(id=user_id)
        return render(request, 'profile.html',{
            'datos': datos
        })

@login_required
def editProfile(request, user_id):
        if request.method == 'GET':
            try:
                datos = User.objects.get(id=user_id)
                datos1 = get_object_or_404(Pagina, user=user_id)
                return render(request, 'edit_profile.html',{
                'datos': datos,
                'datos1': datos1
            })
            except:
                datos = User.objects.get(id=user_id)
                return render(request, 'edit_profile.html',{
                'datos': datos
                })
        else:
            try:
                #link de pagina
                user_id = request.POST['id']
                web = request.POST['web']
                #
                
                #nombre y email del usuario
                name = request.POST['userName']
                if re.search(r'[!@#$%^&*(),.?":{}|<>+]', name):
                    datos = User.objects.get(id=user_id)
                    return render(request, 'edit_profile.html',{
                        'datos': datos,
                        'error': 'Los caracteres especiales no están permitidos en el nombre de usuario.'
                    })
                mail = request.POST['userEmail']
                if re.search(r'[!#$%^&*(),?":{}|<>+]', mail):
                    datos = User.objects.get(id=user_id)
                    return render(request, 'edit_profile.html', {
                        'datos': datos,
                        'error': 'Los caracteres especiales no están permitidos en el correo electrónico.'
                    })
                #
                #Actualizando datos
                datos = User.objects.get(id=user_id)
                datos1 = get_object_or_404(Pagina, user=user_id)
                datos.username = name
                datos.email = mail
                datos1.web = web
                datos1.save()
                datos.save()
                #Volver a tomar capture de pagina web
                options = ChromeOptions()
                options.add_argument("--headless")
                driver = webdriver.Chrome(options=options)

                driver.get(request.POST['web'])

                driver.save_screenshot(f'C:/Users/Usuario/Documents/Cms/django-crud/static/{name}.png')

                driver.quit()

                webpage_content = request.POST['web']
                pagina = Pagina.objects.get(user=user_id)
                if pagina.imagen:
                    os.remove(pagina.imagen.path)
                with open(f'C:/Users/Usuario/Documents/Cms/django-crud/static/{name}.png', 'rb') as f:
                    image_file = SimpleUploadedFile(f.name, f.read())
                    datos1.imagen = image_file
                    datos1.save()
                # Update the Pagina object with the new capture
                pagina = Pagina.objects.get(user=user_id)
                pagina.web = webpage_content
                pagina.imagen = datos1.imagen
                pagina.save()
                #
                return redirect('/')
                #
            except:
                #nombre y email del usuario
                user_id = request.POST['id']
                name = request.POST['userName']
                if re.search(r'[!@#$%^&*(),.?":{}|<>]', name):
                    datos = User.objects.get(id=user_id)
                    return render(request, 'edit_profile.html',{
                        'datos': datos,
                        'error': 'Los caracteres especiales no están permitidos en el nombre de usuario.'
                    })
                mail = request.POST['userEmail']
                if re.search(r'[!#$%^&*(),?":{}|<>]', mail):
                    datos = User.objects.get(id=user_id)
                    return render(request, 'edit_profile.html', {
                        'datos': datos,
                        'error': 'Los caracteres especiales no están permitidos en el correo electrónico.'
                    })
                #
                #Actualizando datos
                datos = User.objects.get(id=user_id)
                datos.username = name
                datos.email = mail
                datos.save()
                return redirect('/')

@login_required
def cambiarContraseña(request, user_id):
    if request.method == 'GET':
        datos = get_object_or_404(User, pk=user_id)
        return render(request, 'solicitar_restablecimiento.html',{
            'datos':datos
        })
    else:
        try:
            user = get_object_or_404(User, pk=user_id)
            email = user.email
            token = default_token_generator.make_token(user)
            token_model = Tokens(user=user, token=token)
            token_model.save()
            print("User ID:", user.pk)
            print("Token:", token)
            reset_url = request.build_absolute_uri(reverse('restablecer_contraseña', args=[user.pk, token]))
            import pdb; pdb.set_trace()
            send_mail(
                'Restablecer tu contraseña',
                        f'Por favor, haz clic en el siguiente enlace para restablecer tu contraseña: {reset_url}',
                        'pruebadedjango46@gmail.com',
                        [email],
                        fail_silently=False
                    )
            return redirect('/')
        except NoReverseMatch as e:
            print(f"Error: {e}")
            
@login_required
def regresarAlInicio(request):
    return redirect('/')
        
# def restablecer_contraseña(request, user_id, token):
    print(f"Request method: {request.method}")
    print(f"Token: {token}")
    print(f"User ID: {user_id}")
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        user.set_password(request.POST['password1'])
        user.save()
        return redirect('signin')
    else:  # Handle GET request
        try:
            user = get_object_or_404(User, pk=user_id)
            tokens = Tokens.objects.filter(user=user_id)
            for token_from_db in tokens:
                if token_from_db.token == token:
                    # Tokens match, render the password reset form
                    return render(request, 'restablecer_contraseña.html',{
                        'datos': token_from_db
                    })
            # Tokens do not match, return an error
            return HttpResponse('Token inválido')
        except User.DoesNotExist:
            return HttpResponse('El usuario no existe')
        except Exception as e:
            return HttpResponse(f'Error: {str(e)}')

@login_required
def restablecer_contraseña(request, user_id, token):
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=user_id)
            tokens = Tokens.objects.get(user=user)
            if tokens.token == token:
                return render(request, 'restablecer_contraseña.html',{
                    'datos': user
                })
            else:
                return HttpResponse('Token inválido')
        except User.DoesNotExist:
            return HttpResponse('El usuario no existe')
        except Exception as e:
            return HttpResponse(f'Error: {str(e)}')
    else:
        user = User.objects.get(pk=user_id)
        user.set_password(request.POST['password1'])
        user.save()
        return redirect('signin')
    
def cambio(request):
    if request.method == 'GET':
        return render(request, 'cambioColor.html')
    else:
        color = request.POST['color']
        new_color = Colores(user=request.user, color_fondo=color)
        new_color.save()
        return redirect('/')
    
def obtenercolor(request):
    color = Colores.objects.get(user = request.user)
    return render(request, 'obtenercolor.html',{
        'color': color
    })