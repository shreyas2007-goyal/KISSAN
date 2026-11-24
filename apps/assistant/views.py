from django.shortcuts import render
from django.http import JsonResponse
from .engine import process_krishi_query

def assistant_chat_view(request):
    lang = getattr(request, 'current_language', 'hi')
    if request.method == 'POST':
        query = request.POST.get('message', '').strip()
        if not query and request.content_type == 'application/json':
            import json
            try:
                data = json.loads(request.body)
                query = data.get('message', '').strip()
            except Exception:
                query = ''
        
        if query:
            answer = process_krishi_query(query, lang=lang)
            return JsonResponse({'status': 'success', 'answer': answer, 'query': query})
        return JsonResponse({'status': 'error', 'message': 'Empty message received.'})

    return render(request, 'assistant/chat.html', {'lang': lang})
