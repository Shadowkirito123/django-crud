from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task, Tokens, UserProfile, Pagina
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from django.utils.crypto import hmac
from django.urls.exceptions import NoReverseMatch
from django.core.files.uploadedfile import SimpleUploadedFile

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
                    
                    options = ChromeOptions()
                    options.add_argument("--headless")
                    driver = webdriver.Chrome(options=options)

                    driver.get(request.POST['web'])

                    driver.save_screenshot(f'C:/Users/Usuario/Desktop/django-crud/tasks/templates/static/{username1}.png')

                    driver.quit()
                    webpage_content = request.POST['web']
                    with open(f'C:/Users/Usuario/Desktop/django-crud/tasks/templates/static/{username1}.png', 'rb') as f:
                        image_file = SimpleUploadedFile(f.name, f.read())
                    Pagina.objects.create(user=user, web=webpage_content, imagen=image_file)
                except:
                    pass
                #
                 
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
    datos1 = get_object_or_404(Pagina, user=user_id)
    return render(request, 'profile.html',{
        'datos': datos,
        'datos1': datos1
    })

@login_required
def editProfile(request, user_id):
        if request.method == 'GET':
            datos = User.objects.get(id=user_id)
            datos1 = get_object_or_404(Pagina, user=user_id)
            return render(request, 'edit_profile.html',{
            'datos': datos,
            'datos1': datos1
        })
        else:
            #link de pagina
            user_id = request.POST['id']
            web = request.POST['web']
            #
            
            #nombre y email del usuario
            user_id = request.POST['id']
            name = request.POST['userName']
            mail = request.POST['userEmail']
            #
            #Actualizando datos
            datos = User.objects.get(id=user_id)
            datos1 = get_object_or_404(Pagina, user=user_id)
            datos.username = name
            datos.email = mail
            datos1.web = web
            datos1.save()
            datos.save()
            return redirect('/')
            #
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
 
 
# def get_universal_tutorial_data(endpoint, api_token, user_email):
#     headers = {
#         "api-token": api_token,
#         "user-email": user_email
#     }
#     response = requests.get(f"https://www.universal-tutorial.com/api/{endpoint}", headers=headers)
#     print(response.text)  # Inspect the raw response

# api_token = "SlxOE6nwU7kPRGFvRUpzI8p2vmHiDtRQTJoMshx_2l33Jl-mWx3vKt8bblxfPUodAO0"
# user_email = "erickrojasmedina2002@gmail.com"

# countries = get_universal_tutorial_data("countries", api_token, user_email)

# def update_profile(request):
#     if request.method == 'POST':
#         # Obtén el token de autorización de Universal Tutorial
#         headers = {
#             "Authorization": "Bearer SlxOE6nwU7kPRGFvRUpzI8p2vmHiDtRQTJoMshx_2l33Jl-mWx3vKt8bblxfPUodAO0",
#             "Accept": "application/json"
#         }

#         # Obtén los datos del país, estado y ciudad de la API
#         country_response = requests.get("https://www.universal-tutorial.com/api/countries/", headers=headers)
#         country_data = country_response.json()

#         state_response = requests.get(f"https://www.universal-tutorial.com/api/states/{country_data['country_name']}", headers=headers)
#         state_data = state_response.json()

#         city_response = requests.get(f"https://www.universal-tutorial.com/api/cities/{state_data['state_name']}", headers=headers)
#         city_data = city_response.json()

#         # Actualiza el perfil del usuario con los datos obtenidos
#         profile = UserProfile.objects.get(user=request.user)
#         profile.country = country_data['country_name']
#         profile.state = state_data['state_name']
#         profile.city = city_data['city_name']
#         profile.save()

#     # Renderiza la plantilla de actualización de perfil
#     return render(request, 'registrar.html')
