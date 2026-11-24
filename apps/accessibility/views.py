from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from .models import UserAccessibilityPreference

@require_http_methods(["GET", "POST"])
def toggle_accessibility(request):
    theme = request.POST.get('theme') or request.GET.get('theme')
    text_size = request.POST.get('text_size') or request.GET.get('text_size')
    simple_mode = request.POST.get('simple_mode') or request.GET.get('simple_mode')

    if theme in ['light', 'dark', 'high-contrast']:
        request.session['a11y_theme'] = theme
    if text_size in ['normal', 'large', 'xlarge']:
        request.session['a11y_text'] = text_size
    if simple_mode is not None:
        is_simple = simple_mode in ['1', 'true', 'yes', 'on']
        request.session['a11y_simple'] = is_simple

    if request.user.is_authenticated:
        pref, _ = UserAccessibilityPreference.objects.get_or_create(user=request.user)
        if theme in ['light', 'dark', 'high-contrast']:
            pref.theme_mode = theme
        if text_size in ['normal', 'large', 'xlarge']:
            pref.text_size = text_size
        if simple_mode is not None:
            pref.simple_farmer_mode = (simple_mode in ['1', 'true', 'yes', 'on'])
        pref.save()

    next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)
