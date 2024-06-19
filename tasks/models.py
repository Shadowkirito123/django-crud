from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='static/', default=None)
    
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