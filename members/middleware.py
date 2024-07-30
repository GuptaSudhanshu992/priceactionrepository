import jwt
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from .models import CustomUser

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/favicon.ico':
            return self.get_response(request)
            
        token = request.COOKIES.get('token')
        
        if token:
            try:
                payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('id')
                if user_id:
                    user = CustomUser.objects.filter(id=user_id).first()
                    request.user = user
                else:
                    request.user = None
            except jwt.ExpiredSignatureError:
                request.user = None
            except jwt.InvalidTokenError:
                request.user = None
        else:
            request.user = None
        response = self.get_response(request)
        return response
