from .dictionary import TRANSLATIONS, get_text

def language_context(request):
    lang = getattr(request, 'current_language', 'hi')
    return {
        'current_language': lang,
        'available_languages': [
            ('en', 'English'),
            ('hi', 'हिंदी (Hindi)'),
            ('pa', 'ਪੰਜਾਬੀ (Punjabi)'),
            ('hr', 'हरियाणवी (Haryanvi Guidance)'),
        ],
        't': TRANSLATIONS.get(lang, TRANSLATIONS['hi']),
        'get_text': lambda key: get_text(key, lang),
    }
