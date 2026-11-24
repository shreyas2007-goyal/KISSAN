from django.db import models
from apps.crops.models import Crop, CropVariety

class SellingComparison(models.Model):
    farmer = models.ForeignKey('farmers.FarmerProfile', on_delete=models.CASCADE, null=True, blank=True, related_name='comparisons')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    variety = models.ForeignKey(CropVariety, on_delete=models.SET_NULL, null=True, blank=True)
    total_quantity_quintals = models.DecimalField(max_digits=10, decimal_places=2, default=50.0)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def best_option(self):
        options = self.options.all()
        if not options:
            return None
        return max(options, key=lambda opt: opt.net_realisation())

    def __str__(self):
        return f"Comparison #{self.id}: {self.crop.name} ({self.total_quantity_quintals} qtl)"

class SellingOption(models.Model):
    class OptionType(models.TextChoices):
        LOCAL_MANDI = 'LOCAL_MANDI', 'Nearby APMC Mandi'
        DISTANT_MANDI = 'DISTANT_MANDI', 'Terminal / Distant High-Price Mandi'
        DIRECT_BUYER = 'DIRECT_BUYER', 'Direct Verified Mill / Trader'
        FPO_COLLECTIVE = 'FPO_COLLECTIVE', 'FPO Collective Selling Lot'
        STORAGE_HOLD = 'STORAGE_HOLD', 'Warehouse Pledge / Deferred Sale'

    comparison = models.ForeignKey(SellingComparison, on_delete=models.CASCADE, related_name='options')
    option_type = models.CharField(max_length=20, choices=OptionType.choices, default=OptionType.LOCAL_MANDI)
    destination_name = models.CharField(max_length=200)
    distance_km = models.DecimalField(max_digits=6, decimal_places=1, default=15.0)
    offered_price_per_quintal = models.DecimalField(max_digits=10, decimal_places=2)
    expected_accepted_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    transport_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    loading_unloading_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    market_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    storage_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    packaging_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    other_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    quality_deduction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def gross_revenue(self):
        return float(self.expected_accepted_quantity) * float(self.offered_price_per_quintal)

    def total_selling_costs(self):
        return (
            float(self.transport_expense) +
            float(self.loading_unloading_expense) +
            float(self.market_fees) +
            float(self.storage_expense) +
            float(self.packaging_expense) +
            float(self.other_expense) +
            float(self.quality_deduction_amount)
        )

    def net_realisation(self):
        return self.gross_revenue() - self.total_selling_costs()

    def net_per_quintal(self):
        qty = float(self.expected_accepted_quantity)
        if qty > 0:
            return round(self.net_realisation() / qty, 2)
        return 0.0

    def __str__(self):
        return f"{self.destination_name} (Net: ₹{self.net_realisation():,.2f})"
