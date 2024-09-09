from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse
from allauth.exceptions import ImmediateHttpResponse

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            if user.auth_method == 'Email':
                messages.error(request, "Email already exists! Please use your credentials to login...")
                raise ImmediateHttpResponse(redirect('login'))
                return super().pre_social_login(request, sociallogin)
        except User.DoesNotExist:
            pass
        
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.email = data.get('email')
        user.firstname = data.get('first_name', '')
        user.lastname = data.get('last_name', '')
        
        provider = sociallogin.account.provider
        
        if provider == 'google':
            user.auth_method = 'Google'
        elif provider == 'facebook':
            user.auth_method = 'Facebook'
        else:
            user.auth_method = provider
        
        return user
