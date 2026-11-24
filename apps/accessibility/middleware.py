from .models import UserAccessibilityPreference

class AccessibilityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow instant session toggle via GET params (e.g. ?theme=dark, ?simple=1, ?text=large)
        if 'theme' in request.GET and request.GET['theme'] in ['light', 'dark', 'high-contrast']:
            request.session['a11y_theme'] = request.GET['theme']
        if 'text_size' in request.GET and request.GET['text_size'] in ['normal', 'large', 'xlarge']:
            request.session['a11y_text'] = request.GET['text_size']
        if 'simple_mode' in request.GET:
            request.session['a11y_simple'] = request.GET['simple_mode'] in ['1', 'true', 'yes']

        theme_mode = request.session.get('a11y_theme', 'light')
        text_size = request.session.get('a11y_text', 'normal')
        simple_farmer_mode = request.session.get('a11y_simple', False)

        # If user is authenticated, override from saved profile unless session had an explicit query override
        if hasattr(request, 'user') and request.user.is_authenticated and not any(k in request.GET for k in ['theme', 'text_size', 'simple_mode']):
            try:
                pref = request.user.accessibility_pref
                theme_mode = pref.theme_mode
                text_size = pref.text_size
                simple_farmer_mode = pref.simple_farmer_mode
            except UserAccessibilityPreference.DoesNotExist:
                pass

        request.a11y = {
            'theme_mode': theme_mode,
            'text_size': text_size,
            'simple_farmer_mode': simple_farmer_mode,
            'voice_assistance': True,
        }

        response = self.get_response(request)
        return response
