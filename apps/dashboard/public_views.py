from django.shortcuts import render
from apps.markets.models import MandiPrice, Mandi
from apps.crops.models import Crop
from apps.schemes.models import Scheme
from apps.buyers.models import BuyerRequirement

def home_view(request):
    featured_prices = MandiPrice.objects.select_related('mandi', 'crop')[:6]
    schemes = Scheme.objects.filter(is_active=True)[:4]
    crops = Crop.objects.all()[:8]
    buyer_offers = BuyerRequirement.objects.filter(is_active=True).select_related('buyer', 'crop')[:4]
    return render(request, 'public/home.html', {
        'featured_prices': featured_prices,
        'schemes': schemes,
        'crops': crops,
        'buyer_offers': buyer_offers,
    })

def about_view(request):
    return render(request, 'public/about.html')

def features_view(request):
    return render(request, 'public/features.html')

def contact_view(request):
    success = False
    if request.method == 'POST':
        success = True
    return render(request, 'public/contact.html', {'success': success})

def faq_view(request):
    return render(request, 'public/faq.html')

def privacy_view(request):
    return render(request, 'public/privacy.html')

def terms_view(request):
    return render(request, 'public/terms.html')

def web3_info_view(request):
    return render(request, 'public/web3_info.html')
