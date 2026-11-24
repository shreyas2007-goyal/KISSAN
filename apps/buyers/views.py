from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BuyerProfile, BuyerRequirement, BuyerEnquiry
from apps.crops.models import Crop

def buyer_list_view(request):
    category = request.GET.get('category')
    state = request.GET.get('state')
    crop_id = request.GET.get('crop')

    buyers = BuyerProfile.objects.all()
    requirements = BuyerRequirement.objects.filter(is_active=True).select_related('buyer', 'crop')

    if category:
        buyers = buyers.filter(category=category)
    if state:
        buyers = buyers.filter(state__iexact=state)
    if crop_id:
        requirements = requirements.filter(crop_id=crop_id)

    crops = Crop.objects.all()
    categories = BuyerProfile.Category.choices

    return render(request, 'buyers/list.html', {
        'buyers': buyers,
        'requirements': requirements,
        'crops': crops,
        'categories': categories,
        'selected_category': category,
        'selected_crop': int(crop_id) if crop_id else None,
    })

def buyer_detail_view(request, buyer_id):
    buyer = get_object_or_404(BuyerProfile, id=buyer_id)
    requirements = BuyerRequirement.objects.filter(buyer=buyer, is_active=True)
    return render(request, 'buyers/detail.html', {
        'buyer': buyer,
        'requirements': requirements,
    })

@login_required
def create_enquiry_view(request, requirement_id):
    requirement = get_object_or_404(BuyerRequirement, id=requirement_id)
    if not hasattr(request.user, 'farmer_profile'):
        messages.error(request, "Only registered farmers can submit procurement enquiries.")
        return redirect('buyers:detail', buyer_id=requirement.buyer.id)

    if request.method == 'POST':
        qty = request.POST.get('quantity')
        rate = request.POST.get('expected_rate')
        notes = request.POST.get('notes', '')

        BuyerEnquiry.objects.create(
            requirement=requirement,
            farmer=request.user.farmer_profile,
            offered_quantity_quintals=qty,
            expected_rate_per_quintal=rate,
            farmer_notes=notes,
        )
        messages.success(request, f"Enquiry submitted to {requirement.buyer.business_name}! The buyer has been notified.")
        return redirect('dashboard:farmer_dashboard')

    return render(request, 'buyers/enquiry_form.html', {'requirement': requirement})
