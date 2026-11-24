def accessibility_context(request):
    a11y = getattr(request, 'a11y', {
        'theme_mode': 'light',
        'text_size': 'normal',
        'simple_farmer_mode': False,
        'voice_assistance': True,
    })
    return {
        'a11y': a11y,
        'is_simple_mode': a11y.get('simple_farmer_mode', False),
        'theme_class': f"theme-{a11y.get('theme_mode', 'light')} font-{a11y.get('text_size', 'normal')} {'mode-simple-farmer' if a11y.get('simple_farmer_mode') else ''}",
    }
