from django.urls import path, include
from .views import RegisterView, LoginView, UserView, LogoutView, ForgotPasswordView, ResetPasswordView, Register_API, Login_API, Logout_API, g_social_login 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgotpassword/', ForgotPasswordView.as_view(), name='forgotpassword'),
    path('resetpassword/<uidb64>/<token>/', ResetPasswordView.as_view(), name='resetpassword'),
    path('resetpassword/', ResetPasswordView.as_view(), name='resetpasswordconfirmed'),
    
    #social account login
    path('g_social_login/', g_social_login, name='g_social_login'),
    
    #Mobile APIs
    path('api/v1/register/', Register_API, name='register_api'),
    path('api/v1/login/', Login_API, name='login_api'),
    path('api/v1/logout/', Logout_API, name='logout_api'),
]