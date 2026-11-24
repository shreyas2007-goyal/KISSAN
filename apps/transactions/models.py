from django.db import models
from apps.crops.models import Crop, CropVariety

class Transaction(models.Model):
    class Status(models.TextChoices):
        COMPLETED = 'COMPLETED', 'Payment Cleared & Delivered'
        PENDING = 'PENDING', 'Weighment Completed - Payment Processing'
        DISPUTED = 'DISPUTED', 'Under Review / Quality Discrepancy'

    farmer = models.ForeignKey('farmers.FarmerProfile', on_delete=models.CASCADE, related_name='transactions')
    buyer = models.ForeignKey('buyers.BuyerProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='procurement_transactions')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    variety = models.ForeignKey(CropVariety, on_delete=models.SET_NULL, null=True, blank=True)
    quantity_quintals = models.DecimalField(max_digits=10, decimal_places=2)
    agreed_rate_per_quintal = models.DecimalField(max_digits=10, decimal_places=2)
    gross_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total_deductions_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    net_payable_to_farmer = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.COMPLETED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TXN #{self.id}: {self.crop.name} ({self.quantity_quintals} qtl) - ₹{self.net_payable_to_farmer:,.2f}"
