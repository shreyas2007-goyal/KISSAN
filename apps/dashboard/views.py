from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.models import User
from apps.markets.models import MandiPrice
from apps.schemes.models import Scheme
from apps.farmers.models import FarmerProfile, FarmerCrop
from apps.buyers.models import BuyerRequirement, BuyerEnquiry
from apps.fpos.models import FPO, FPOCropLot
from apps.calculator.models import SellingComparison
from apps.crop_wellness.models import CropHealthAnalysis
from apps.transactions.models import Transaction

@login_required
def dashboard_dispatcher(request):
    role = request.user.role
    if role == User.Role.PLATFORM_ADMIN or request.user.is_superuser:
        return redirect('dashboard:admin_dashboard')
    elif role == User.Role.BUYER:
        return redirect('dashboard:buyer_dashboard')
    elif role == User.Role.FPO_ADMIN:
        return redirect('dashboard:fpo_dashboard')
    else:
        return redirect('dashboard:farmer_dashboard')

@login_required
def farmer_dashboard(request):
    farmer_profile, _ = FarmerProfile.objects.get_or_create(user=request.user)
    my_crops = FarmerCrop.objects.filter(farmer=farmer_profile)
    latest_prices = MandiPrice.objects.filter(mandi__district=farmer_profile.district)[:5]
    if not latest_prices:
        latest_prices = MandiPrice.objects.all()[:5]
    
    comparisons = SellingComparison.objects.filter(farmer=farmer_profile)[:3]
    recent_screenings = CropHealthAnalysis.objects.filter(farmer=farmer_profile)[:3]
    transactions = Transaction.objects.filter(farmer=farmer_profile)[:4]
    buyer_offers = BuyerRequirement.objects.filter(is_active=True)[:4]

    return render(request, 'farmer/dashboard.html', {
        'farmer': farmer_profile,
        'my_crops': my_crops,
        'latest_prices': latest_prices,
        'comparisons': comparisons,
        'recent_screenings': recent_screenings,
        'transactions': transactions,
        'buyer_offers': buyer_offers,
    })

@login_required
def buyer_dashboard(request):
    if not (request.user.is_buyer() or request.user.is_admin_user()):
        return redirect('dashboard:farmer_dashboard')
    buyer_profile, _ = request.user.buyer_profile if hasattr(request.user, 'buyer_profile') else (None, None)
    requirements = BuyerRequirement.objects.filter(buyer=buyer_profile) if buyer_profile else []
    enquiries = BuyerEnquiry.objects.filter(requirement__buyer=buyer_profile) if buyer_profile else []

    return render(request, 'buyer/dashboard.html', {
        'buyer': buyer_profile,
        'requirements': requirements,
        'enquiries': enquiries,
    })

@login_required
def fpo_dashboard(request):
    if not (request.user.is_fpo() or request.user.is_admin_user()):
        return redirect('dashboard:farmer_dashboard')
    fpo_profile = getattr(request.user, 'fpo_profile', None)
    lots = FPOCropLot.objects.filter(fpo=fpo_profile) if fpo_profile else []
    members = fpo_profile.memberships.select_related('farmer__user').all() if fpo_profile else []

    return render(request, 'fpo/dashboard.html', {
        'fpo': fpo_profile,
        'lots': lots,
        'members': members,
    })

@login_required
def admin_dashboard(request):
    if not request.user.is_admin_user():
        return redirect('dashboard:farmer_dashboard')
    
    total_users = User.objects.count()
    total_farmers = FarmerProfile.objects.count()
    total_buyers = User.objects.filter(role=User.Role.BUYER).count()
    total_transactions = Transaction.objects.count()
    recent_analyses = CropHealthAnalysis.objects.all()[:5]

    return render(request, 'admin_custom/dashboard.html', {
        'total_users': total_users,
        'total_farmers': total_farmers,
        'total_buyers': total_buyers,
        'total_transactions': total_transactions,
        'recent_analyses': recent_analyses,
    })
