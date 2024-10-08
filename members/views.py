from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, base36_to_int
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from .tokens import account_activation_token
import re
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
import requests

User = get_user_model()

class RegisterView(View):    
    def get(self, request, *args, **kwargs):
        if request.user is not None:
            if request.user.is_authenticated:
                return redirect('/blog/')
        return render(request=request, template_name='members/signup.html')
        
    def post(self, request, *args, **kwargs):
        try:
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            auth_method = request.POST.get('auth_method')
            referrer = request.POST.get('referrer')
            is_pwd_valid, password_validation_message = is_password_valid(password1, password2)
            if not firstname or not email or not password1 or not password2:
                message = 'All fields are required.'
            elif User.objects.filter(email=email).exists():
                message = 'Email is already registered.'
            elif not is_pwd_valid:
                message = password_validation_message
            else:
                user = User.objects.create_user(
                    email=email,
                    password=password1,
                    firstname=firstname,
                    lastname=lastname,
                    auth_method=auth_method
                )
                user.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                send_welcome_email(request, email, firstname, lastname)
                return JsonResponse({
                    'success': True,
                    'message':'Congratulations, You have registered successfully, Welcome to the team!<br>Redirecting in 2 seconds...',
                    'redirect_url':referrer,
                })
            return JsonResponse({
                        'success': False,
                        'message': message,
                    })
        except ValidationError as e:
            return JsonResponse({
                'success': False,
                'message': f'Error Occurred : {str(e)}',
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error Occurred : {str(e)}',
            })

class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user is not None:
            if request.user.is_authenticated:
                return redirect('/blog/')
        return render(request=request, template_name='members/login.html')
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        referrer = request.POST.get('referrer', "{% url 'blog' %}")
        
        if User.objects.filter(email=email).exists():
            if User.objects.get(email=email).auth_method == 'Email':
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    return JsonResponse({
                        'success': True,
                        'message':'Login Successful! Redirecting in 2 seconds...',
                        'redirect_url': referrer
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message':'Invalid Email or Password, please try again...',
                    })
            else:
                return JsonResponse({
                        'success': False,
                        'message':'Please use your social account, to login to the application...',
                    })
        else:
            return JsonResponse({
                    'success': False,
                    'message':'Email address is not registered with us...',
                })

class UserView(View):
    def get(self, request, *args, **kwargs):
        return null

class LogoutView(View):
    def post(self, request, *args, **kwargs):
        try:
            referrer = request.POST.get('referrer', "{% url 'blog' %}")
            logout(request)
            return JsonResponse({
                    'success': True,
                    'message':'Logged out successfully!',
                    'redirect_url':referrer
                })
        except Exception as e:
            return JsonResponse({
                    'success': False,
                    'message':'Error Occurred while logging out, please refresh the page and try again!',
                    'error':str(e)
                })
            
class ForgotPasswordView(View):
    def get(self, request, *args, **kwargs):
        if request.user is not None:
            if request.user.is_authenticated:
                return redirect('/blog/')
        return render(request=request, template_name='members/forgotpassword.html')
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        referrer = request.POST.get('referrer')
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(reverse('resetpassword', kwargs={'uidb64': uid, 'token': token}))
            messages.success(request, 'An Email with a link to reset your password has been sent to your registered email address, kindly use that link to reset your password. Please note that the link is valid only for 15 minutes.')
            message = 'An Email with a link to reset your password has been sent to your registered email address, kindly use that link to reset your password. Please note that the link is valid only for 15 minutes.'
            send_reset_password_email(request, email, user.firstname, user.lastname, reset_link)
            return JsonResponse({
                    'success': True,
                    'message': message,
                    'redirect_url': referrer
                })
        else:
            messages.warning(request, 'The email you entered is not registered with us!')
            message = 'The email you entered is not registered with us!'
            return JsonResponse({
                    'success': False,
                    'message': message
                })

class ResetPasswordView(View):
    def get(self, request, uidb64=None, token=None):
        if uidb64 is None or token is None:
            messages.warning(request,"Invalid Password Reset Link")
            return redirect('/members/login/')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
    
        if user is not None:# and account_activation_token.check_token(user, token):
            return render(request, 'members/reset_password.html', {'uidb64': uidb64, 'token': token})
        else:
            return HttpResponse("Invalid Reset Link")
    
    def post(self, request, *args, **kwargs):
        uidb64 = request.POST.get('uidb64')
        token = request.POST.get('token')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        referrer = request.POST.get('referrer')
        is_pwd_valid, pwd_validation_msg = is_password_valid(password1, password2)
        if not is_pwd_valid:
            message=pwd_validation_msg
        else:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                
                if user is not None: #and account_activation_token.check_token(user, token):
                    user.set_password(password1)
                    user.save()
                    message='Your password has been reset successfully. You can now log in with the new password.'
                    return JsonResponse({
                    'success': True,
                    'message': message,
                    'redirect_url': referrer
                    })
                else:
                    message='Invalid password reset link.'
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
                message='User not found!'
        return JsonResponse({
                    'success': False,
                    'message': message,
                    'uidb64': uidb64,
                    'token': token
                    })
                    
@csrf_exempt
@require_POST
def g_social_login(request, *args, **kwargs):
    try:
        id_token = request.POST.get('id_token')
        auth_method = 'Google'
        referrer = request.POST.get('referrer','/blog/')
        
        token_verification_url = f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}'
        response = requests.get(token_verification_url)
        token_info = response.json()

        email = token_info['email']
        firstname = token_info['given_name']
        lastname = token_info['family_name']
        is_verified = token_info['email_verified']
        if 'error_description' in token_info:
            return JsonResponse({'success': False, 'message': token_info["error_description"]}, status=400)
            
        try:
            user = User.objects.get(email=email, auth_method=auth_method)
        except:
            user = User.objects.create_user(
                email=email,
                firstname=firstname,
                lastname=lastname,
                auth_method=auth_method,
                is_verified=True
            )
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            send_welcome_email(request, email, firstname, lastname)
            return JsonResponse({
                'success': True,
                'message':'Congratulations, You have registered successfully, Welcome to the team!<br>Redirecting in 2 seconds...',
                'redirect_url':referrer,
            })
            
        if user is not None:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return JsonResponse({
                'success': True,
                'message':'Login Successful! Redirecting in 2 seconds...',
                'redirect_url': referrer
            })
        else:
            return JsonResponse({
                'success': False,
                'message':'User does not exist'
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })
    
@csrf_exempt
@require_POST
def Register_API(request, *args, **kwargs):
    if request.method == 'POST':
        register_view = RegisterView.as_view()
        response = register_view(request)
        return response
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
        
@csrf_exempt
@require_POST
def Login_API(request, *args, **kwargs):
    print("Request Method is : ", request.method)
    if request.method == 'POST':
        login_view = LoginView.as_view()
        response = login_view(request)
        return response
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
@csrf_exempt
@require_POST
def Logout_API(request, *args, **kwargs):
    if request.method == 'POST':
        logout_view = LogoutView.as_view()
        response = logout_view(request)
        return response
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
 
def is_password_valid(password1, password2):
    if password1 != password2:
        return False, 'Password and Confirm password must match.'

    if len(password1) < 6 or len(password1) > 20:
        return False, 'Password should be between 6 and 20 characters in length.'

    if not bool(re.search(r'[A-Z]', password1)):
        return False, 'Password is missing an uppercase letter'

    if not bool(re.search(r'[a-z]', password1)):
        return False, 'Password is missing a lowercase letter'

    if not bool(re.search(r'[0-9]', password1)):
        return False, 'Password must contain at least one digit.'

    if not bool(re.search(r'[!@#$%^&*()_+{}[\]:;"\'<>,.?~`]', password1)):
        return False, 'Password must contain one of these special characters [!@#$%^&*()_+{}[\]:;"\'<>,.?~`]'

    return True, 'Password is Valid'
        
def send_reset_password_email(request, recipient_email, firstname, lastname, reset_link):
    subject = 'Reset your password'
    from_email = 'admin@equityanalysis.co.in'
    recipient_list = [recipient_email]
    text_content = 'Reset your password!'
    html_content = render_to_string('members/email_reset_password.html', {
        'firstname': firstname,
        'lastname': lastname,
        'reset_link': reset_link,
    })
    try:
        email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        email.attach_alternative(html_content, 'text/html')
        email.send()
    except Exception as e:
        print(str(e))
    return HttpResponse('HTML Email sent successfully!')
    
def send_welcome_email(request, recipient_email, firstname, lastname):
    subject = 'Welcome to the team!'
    from_email = 'admin@equityanalysis.co.in'
    recipient_list = [recipient_email]
    text_content = 'Welcome to the team!'
    html_content = render_to_string('members/email_welcome_template.html', {
        'firstname': firstname,
        'lastname': lastname,
    })
    try:
        email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        email.content_subtype = "html"
        email.attach_alternative(html_content, 'text/html')
        email.send()
    except Exception as e:
        print(str(e))
    return HttpResponse('HTML Email sent successfully!')