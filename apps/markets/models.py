from django.db import models
from apps.crops.models import Crop, CropVariety

class Mandi(models.Model):
    name = models.CharField(max_length=150)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    market_type = models.CharField(max_length=50, default='APMC Principal Yard')
    market_fee_percent = models.DecimalField(max_digits=4, decimal_places=2, default=1.00, help_text="APMC User/Market Cess %")
    unloading_charge_per_quintal = models.DecimalField(max_digits=6, decimal_places=2, default=15.00, help_text="Labour / Palledari per Quintal")
    address = models.TextField(blank=True)

    class Meta:
        unique_together = ('name', 'district', 'state')

    def __str__(self):
        return f"{self.name} ({self.district}, {self.state})"

class MandiPrice(models.Model):
    class Source(models.TextChoices):
        AGMARKNET = 'AGMARKNET', 'Agmarknet (Govt of India)'
        DATA_GOV_IN = 'DATA_GOV_IN', 'Open Government Data (data.gov.in)'
        APMC_DIRECT = 'APMC_DIRECT', 'APMC Daily Electronic Ticker'
        DEMO = 'DEMO_DATA', 'Verified Sample / Demonstration Data'

    mandi = models.ForeignKey(Mandi, on_delete=models.CASCADE, related_name='prices')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='mandi_prices')
    variety = models.ForeignKey(CropVariety, on_delete=models.SET_NULL, null=True, blank=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    modal_price = models.DecimalField(max_digits=10, decimal_places=2)
    arrival_quantity_quintals = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    price_date = models.DateField()
    source = models.CharField(max_length=30, choices=Source.choices, default=Source.DEMO)
    is_demo_data = models.BooleanField(default=True)
    retrieved_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['crop', 'price_date']),
            models.Index(fields=['mandi', 'price_date']),
        ]
        ordering = ['-price_date', '-retrieved_at']

    def __str__(self):
        return f"{self.crop.name} @ {self.mandi.name}: ₹{self.modal_price}/qtl ({self.price_date})"
