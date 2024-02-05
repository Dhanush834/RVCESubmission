# myapp/urls.py
from django.urls import path
from .views import run_python_program
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('run-python-program/', run_python_program, name='run_python_program'),
    
]
