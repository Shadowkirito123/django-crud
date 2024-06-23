from django.forms import ModelForm
from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Escribe un titulo'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Escribe un titulo'}),
            # 'important': forms.CheckboxInput(attrs={'class': 'form-control'})
        }