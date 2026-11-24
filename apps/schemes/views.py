from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Scheme, SchemeBookmark

def scheme_list_view(request):
    query = request.GET.get('q', '')
    level = request.GET.get('level', '')
    state = request.GET.get('state', '')

    schemes = Scheme.objects.filter(is_active=True)
    if query:
        schemes = schemes.filter(name__icontains=query) | schemes.filter(objective__icontains=query)
    if level:
        schemes = schemes.filter(level=level)
    if state:
        schemes = schemes.filter(applicable_state__icontains=state)

    states = Scheme.objects.values_list('applicable_state', flat=True).distinct()

    return render(request, 'schemes/list.html', {
        'schemes': schemes,
        'query': query,
        'level': level,
        'state': state,
        'states': states,
    })

def scheme_detail_view(request, scheme_id):
    scheme = get_object_or_404(Scheme, id=scheme_id)
    is_bookmarked = False
    if request.user.is_authenticated and hasattr(request.user, 'farmer_profile'):
        is_bookmarked = SchemeBookmark.objects.filter(farmer=request.user.farmer_profile, scheme=scheme).exists()
    return render(request, 'schemes/detail.html', {
        'scheme': scheme,
        'is_bookmarked': is_bookmarked,
    })

def scheme_eligibility_view(request):
    results = None
    if request.method == 'POST':
        land_size = float(request.POST.get('land_size', 2.0))
        is_fpo = request.POST.get('is_fpo') == 'yes'
        crop_type = request.POST.get('crop_type', 'Cereal')

        matched_schemes = []
        for s in Scheme.objects.filter(is_active=True):
            status = 'Potentially Eligible'
            if 'PM-KISAN' in s.name:
                status = 'High Probability Match' if land_size <= 5.0 else 'Eligible'
            elif 'FPO' in s.name:
                status = 'High Probability Match' if is_fpo else 'Requires FPO Membership'
            elif 'Fasal Bima' in s.name:
                status = 'High Probability Match'
            
            matched_schemes.append({
                'scheme': s,
                'status': status,
            })
        results = matched_schemes

    return render(request, 'schemes/eligibility.html', {'results': results})

@login_required
def scheme_bookmark_toggle(request, scheme_id):
    scheme = get_object_or_404(Scheme, id=scheme_id)
    if hasattr(request.user, 'farmer_profile'):
        bookmark = SchemeBookmark.objects.filter(farmer=request.user.farmer_profile, scheme=scheme)
        if bookmark.exists():
            bookmark.delete()
            messages.info(request, "Scheme removed from your bookmarks.")
        else:
            SchemeBookmark.objects.create(farmer=request.user.farmer_profile, scheme=scheme)
            messages.success(request, "Scheme saved to your bookmarks!")
    return redirect('schemes:detail', scheme_id=scheme.id)
