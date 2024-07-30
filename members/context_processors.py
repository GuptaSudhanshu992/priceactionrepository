def user_status(request):
    if request.user is None:
        return {
            'user_is_authenticated': False
        }
    else:
        return {
            'user_is_authenticated': request.user.is_authenticated
        }
