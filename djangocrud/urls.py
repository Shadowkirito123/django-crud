"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_complete/', views.tasks_complete, name='task_complete'),
    path('tasks/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signip, name='signin'),
    path('createtask/', views.create_task, name='createtask'),
    path('tasks/<int:task_id>', views.task_detail, name='task detail'),
    path('usuario/<int:user_id>', views.perfil, name='usuario'),
    path('editarUsuario/<int:user_id>', views.editProfile, name='edit_usuario'),
    path('solicitarContra/<int:user_id>', views.solicitarRestablecerContra, name='solicitarContraseña'),
    path('restablacerClave/<int:user_id>', views.restablecer_contraseña, name='restablecerContra')
]
