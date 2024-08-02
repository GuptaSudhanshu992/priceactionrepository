from django.shortcuts import render, redirect
from django.views import View
from .models import CustomUser
import jwt, datetime
from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
import re

User = get_user_model()

class RegisterView(View):    
    def get(self, request):
        if request.user is not None:
            if request.user.is_authenticated:
                messages.info(request, 'Hi, You already seemed to be logged in from an account, kindly logout if you want to create a new account!')
                return redirect('/blog/')
        return render(request=request, template_name='members/signup.html')
        
    def post(self, request):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not firstname or not email or not password1 or not password2:
            messages.warning(request, 'All fields are required.')
        elif User.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already registered.')
        elif len(password1)<6 or len(password1)>20:
            messages.warning(request, 'Password should be between 6 and 20 characters in length.')
        elif not bool(re.search(r'[A-Z]', password1)):
            messages.warning(request, 'Password is missing an uppercase letter')
        elif not bool(re.search(r'[a-z]', password1)):
            messages.warning(request, 'Password is missing a lowercase letter')
        elif not bool(re.search(r'[0-9]', password1)):
            messages.warning(request, 'Password must contain at least one digit.')
        elif not bool(re.search(r'[!@#$%^&*()_+{}\[\]:;"\'<>,.?~`]', password1)):
            messages.warning(request, 'Password must contain one of these special characters [!@#$%^&*()_+{}\[\]:;"\'<>,.?~`]')
        elif password1 != password2:
            messages.warning(request, 'Passwords do not match.')
        else:
            try:
                user = User.objects.create_user(
                    email=email,
                    password=password1,
                    firstname=firstname,
                    lastname=lastname
                )
                user.save()
                login(request, user)
                messages.success(request, 'You have registered successfully, Welcome to the team!')
                return redirect('/blog/')
            except ValidationError as e:
                messages.warning(request, str(e))
            except Exception as e:
                messages.warning(request, str(e))
        return render(request=request, template_name='members/signup.html')

class LoginView(View):
    def get(self, request):
        if request.user is not None:
            if request.user.is_authenticated:
                messages.info(request, 'Please logout first, if you want to login from a different account.')
                return redirect('/blog/')
        return render(request=request, template_name='members/login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('/blog/')
        else:
            messages.warning(request, 'Invalid email or password.')
        return render(request=request, template_name='members/login.html')

class UserView(View):
    def get(self, request):
        return null

class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'Logged Out Successfully!')
        return redirect('/blog/')