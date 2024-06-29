from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextUploadingField(default=None)
    # description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title + ' - ' + self.user.username

class Tokens(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField()

class Pagina(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    web = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='static/', default=None)
    
    def __str__(self):
        return self.web

class Colores(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color_fondo = models.CharField(max_length=7)
    
    def __str__(self):
        return self.color_fondo
    
class Comentarios(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True, default=None)

    def __str__(self) :
        return self.comment
    