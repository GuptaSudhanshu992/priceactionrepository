def current_url(request):
    return {
        'current_url': request.build_absolute_uri()
    }
