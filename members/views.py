from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from .serializers import UserSerializer
from .models import CustomUser
import jwt, datetime
from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest

class RegisterView(APIView):    
    def get(self, request):
        return render(request, 'members/signup.html')
        
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        messages.success(request, 'Registration successful!')
        
        login_view = LoginView()
        login_response = login_view.post(request)
        
        if login_response.status_code == 200:
            response = redirect('blog')
            response.set_cookie(key="token", value=login_response.data['token'], httponly=True, max_age=60*60*24*7)
            return response
        else:
            messages.error(request, 'Registration in completed, you may log into your account now.')
            return redirect('login')

class LoginView(APIView):
    def get(self, request):
        return render(request, 'members/login.html')
    
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        user = CustomUser.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed('User not found!')
            
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')
        
        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, settings.JWT_SECRET_KEY , algorithm='HS256')
        messages.success(request, 'Welcome Back!')
        response = Response({
            "message":"success",
            "token":token,
        })
        response = redirect('blog')
        response.set_cookie(key="token", value=token, httponly=True, max_age=60*60*24*7)
        return response

class UserView(APIView):
    def get(self, request):
        token=request.COOKIES.get('token')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
            
        user = CustomUser.objects.filter(id=payload['id']).first()
        
        serializer = UserSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response({
            'message':'success'
        })
        response = redirect('blog')
        response.delete_cookie('token')
        return response