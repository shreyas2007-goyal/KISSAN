class MultilingualMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Check URL query param ?lang=
        lang = request.GET.get('lang')
        if lang in ['en', 'hi', 'pa', 'hr']:
            request.session['django_language'] = lang
        elif 'django_language' in request.session:
            lang = request.session['django_language']
        elif hasattr(request, 'user') and request.user.is_authenticated and hasattr(request.user, 'preferred_language'):
            lang = request.user.preferred_language
        else:
            lang = 'hi'  # Default to Hindi for inclusive Indian farming audience
        
        request.current_language = lang
        response = self.get_response(request)
        return response
