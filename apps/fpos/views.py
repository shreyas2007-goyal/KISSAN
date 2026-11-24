from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FPO, FPOCropLot, FPOMembership, FPOMemberContribution
from apps.crops.models import Crop

def fpo_list_view(request):
    fpos = FPO.objects.filter(is_verified=True).prefetch_related('lots')
    return render(request, 'fpo/list.html', {'fpos': fpos})

def fpo_detail_view(request, fpo_id):
    fpo = get_object_or_404(FPO, id=fpo_id)
    lots = FPOCropLot.objects.filter(fpo=fpo)
    is_member = False
    if request.user.is_authenticated and hasattr(request.user, 'farmer_profile'):
        is_member = FPOMembership.objects.filter(fpo=fpo, farmer=request.user.farmer_profile).exists()
    return render(request, 'fpo/detail.html', {
        'fpo': fpo,
        'lots': lots,
        'is_member': is_member,
    })

@login_required
def join_fpo_view(request, fpo_id):
    fpo = get_object_or_404(FPO, id=fpo_id)
    if hasattr(request.user, 'farmer_profile'):
        membership, created = FPOMembership.objects.get_or_create(fpo=fpo, farmer=request.user.farmer_profile)
        if created:
            messages.success(request, f"Congratulations! You are now a registered member of {fpo.name}.")
        else:
            messages.info(request, f"You are already a registered shareholder member of {fpo.name}.")
    else:
        messages.error(request, "Only registered farmer profiles can join an FPO.")
    return redirect('fpo:detail', fpo_id=fpo.id)
