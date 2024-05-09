from django import forms
from django.forms import ModelForm
from .models import Todo

class CreateTodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'due_time', 'is_important']
        widgets = {
            'due_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }