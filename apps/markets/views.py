from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Min, Max
from .models import Mandi, MandiPrice
from apps.crops.models import Crop

def market_list_view(request):
    crop_id = request.GET.get('crop')
    state = request.GET.get('state')
    district = request.GET.get('district')

    prices = MandiPrice.objects.select_related('mandi', 'crop')

    if crop_id:
        prices = prices.filter(crop_id=crop_id)
    if state:
        prices = prices.filter(mandi__state__iexact=state)
    if district:
        prices = prices.filter(mandi__district__iexact=district)

    crops = Crop.objects.all()
    states = Mandi.objects.values_list('state', flat=True).distinct()
    districts = Mandi.objects.values_list('district', flat=True).distinct()

    return render(request, 'markets/list.html', {
        'prices': prices[:50],
        'crops': crops,
        'states': states,
        'districts': districts,
        'selected_crop': int(crop_id) if crop_id else None,
        'selected_state': state,
        'selected_district': district,
    })

def market_detail_view(request, mandi_id):
    mandi = get_object_or_404(Mandi, id=mandi_id)
    prices = MandiPrice.objects.filter(mandi=mandi).select_related('crop')
    return render(request, 'markets/detail.html', {
        'mandi': mandi,
        'prices': prices,
    })

def market_compare_view(request):
    crop_id = request.GET.get('crop')
    crop = Crop.objects.filter(id=crop_id).first() if crop_id else Crop.objects.first()
    
    comparisons = []
    if crop:
        comparisons = MandiPrice.objects.filter(crop=crop).select_related('mandi').order_by('-modal_price')[:10]

    crops = Crop.objects.all()
    return render(request, 'markets/compare.html', {
        'crop': crop,
        'crops': crops,
        'comparisons': comparisons,
    })
