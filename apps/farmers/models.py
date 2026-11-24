from django.db import models
from django.conf import settings
from apps.crops.models import Crop, CropVariety

class FarmerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='farmer_profile')
    state = models.CharField(max_length=100, default='Haryana')
    district = models.CharField(max_length=100, default='Karnal')
    village = models.CharField(max_length=100, blank=True)
    landholding_acres = models.DecimalField(max_digits=6, decimal_places=2, default=2.5)
    irrigation_source = models.CharField(max_length=50, default='Tube Well / Borewell')
    soil_type = models.CharField(max_length=50, default='Alluvial Loam')
    has_kcc = models.BooleanField(default=False, verbose_name="Kisan Credit Card (KCC) Holder")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Farmer: {self.user.get_full_name() or self.user.username} ({self.district}, {self.state})"

class FarmerCrop(models.Model):
    class Status(models.TextChoices):
        SOWN = 'SOWN', 'Sown / Boyi Gayi'
        VEGETATIVE = 'VEGETATIVE', 'Vegetative Growth / Vridhi'
        FLOWERING = 'FLOWERING', 'Flowering / Phool'
        HARVEST_READY = 'HARVEST_READY', 'Ready for Harvest / Kataai Hetu Taiyar'
        HARVESTED = 'HARVESTED', 'Harvested in Storage / Kataai Sampann'
        SOLD = 'SOLD', 'Sold / Bikri Sampann'

    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='crops')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    variety = models.ForeignKey(CropVariety, on_delete=models.SET_NULL, null=True, blank=True)
    acres = models.DecimalField(max_digits=6, decimal_places=2, default=1.0)
    sowing_date = models.DateField()
    expected_harvest_date = models.DateField(null=True, blank=True)
    estimated_quantity_quintals = models.DecimalField(max_digits=8, decimal_places=2, default=20.0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.VEGETATIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop.name} - {self.acres} Acres ({self.farmer.user.username})"
