from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect
from django.db import IntegrityError
from django.http import HttpResponse
import logging


# Create your views here.

def index(request):
    return render(request, 'index.html')


def download(request):
    return render(request, 'download.html')


logger = logging.getLogger(__name__)


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = make_password(request.POST.get('password'))
        contact = request.POST.get('contact')

        try:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered. Please login.')
            else:
                user = User(name=name, email=email, password=password, contact=contact)
                user.save()
                messages.success(request, 'Registration successful! Please login.')
                return redirect('login')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                messages.success(request, 'Login successful')
                return redirect('index')
            else:
                messages.error(request, 'Invalid credentials')
        except User.DoesNotExist:
            messages.error(request, 'User not found')

    return render(request, 'login.html')
