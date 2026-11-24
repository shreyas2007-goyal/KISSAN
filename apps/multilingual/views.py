from django.shortcuts import redirect

def switch_language(request, lang_code):
    if lang_code in ['en', 'hi', 'pa', 'hr']:
        request.session['django_language'] = lang_code
        if request.user.is_authenticated:
            request.user.preferred_language = lang_code
            request.user.save(update_fields=['preferred_language'])
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)
