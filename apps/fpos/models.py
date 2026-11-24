from django.db import models
from django.conf import settings
from apps.crops.models import Crop

class FPO(models.Model):
    admin_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fpo_profile')
    name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=100, unique=True, help_text="CIN / Society Registration Number")
    state = models.CharField(max_length=100, default='Haryana')
    district = models.CharField(max_length=100, default='Karnal')
    headquarters = models.CharField(max_length=200, default='Taraori Road, Karnal')
    contact_phone = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_members(self):
        return self.memberships.count()

    def __str__(self):
        return f"{self.name} ({self.district}, {self.state})"

class FPOMembership(models.Model):
    fpo = models.ForeignKey(FPO, on_delete=models.CASCADE, related_name='memberships')
    farmer = models.ForeignKey('farmers.FarmerProfile', on_delete=models.CASCADE, related_name='fpo_memberships')
    share_units = models.PositiveIntegerField(default=10)
    joined_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('fpo', 'farmer')

    def __str__(self):
        return f"{self.farmer.user.username} in {self.fpo.name}"

class FPOCropLot(models.Model):
    class Status(models.TextChoices):
        AGGREGATING = 'AGGREGATING', 'Aggregating Member Stock'
        LOT_READY = 'LOT_READY', 'Lot Formed & Quality Graded'
        OFFERED_TO_BUYERS = 'OFFERED', 'Offered to Institutional Buyers'
        SOLD = 'SOLD', 'Contract Finalized & Sold'
        SETTLED = 'SETTLED', 'Payments Disbursed to Members'

    fpo = models.ForeignKey(FPO, on_delete=models.CASCADE, related_name='lots')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    lot_code = models.CharField(max_length=50, unique=True)
    aggregated_quantity_quintals = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    target_price_per_quintal = models.DecimalField(max_digits=10, decimal_places=2)
    quality_grade = models.CharField(max_length=50, default='Grade A - FAQ (Fair Average Quality)')
    storage_facility = models.CharField(max_length=200, default='FPO Central Warehouse, Taraori')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AGGREGATING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lot_code}: {self.crop.name} ({self.aggregated_quantity_quintals} qtl)"

class FPOMemberContribution(models.Model):
    lot = models.ForeignKey(FPOCropLot, on_delete=models.CASCADE, related_name='contributions')
    farmer = models.ForeignKey('farmers.FarmerProfile', on_delete=models.CASCADE)
    contributed_quantity_quintals = models.DecimalField(max_digits=10, decimal_places=2)
    received_payment_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    disbursed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.farmer.user.username} -> {self.lot.lot_code}: {self.contributed_quantity_quintals} qtl"
