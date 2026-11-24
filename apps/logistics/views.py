from django.shortcuts import render
from .models import StorageFacility, Transporter

def logistics_index_view(request):
    facility_type = request.GET.get('facility_type')
    district = request.GET.get('district')

    storages = StorageFacility.objects.all()
    transporters = Transporter.objects.filter(is_verified=True)

    if facility_type:
        storages = storages.filter(facility_type=facility_type)
    if district:
        storages = storages.filter(district__iexact=district)
        transporters = transporters.filter(operating_district__iexact=district)

    districts = StorageFacility.objects.values_list('district', flat=True).distinct()

    return render(request, 'logistics/index.html', {
        'storages': storages,
        'transporters': transporters,
        'districts': districts,
        'facility_types': StorageFacility.FacilityType.choices,
        'selected_district': district,
        'selected_type': facility_type,
    })
