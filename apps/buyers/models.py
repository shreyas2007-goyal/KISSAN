from django.db import models
from django.conf import settings
from apps.crops.models import Crop, CropVariety

class BuyerProfile(models.Model):
    class Category(models.TextChoices):
        LOCAL_TRADER = 'LOCAL_TRADER', 'Local Mandi Trader / Vyapari'
        WHOLESALER = 'WHOLESALER', 'Wholesale Commission Agent / Arhtiya'
        FOOD_PROCESSOR = 'FOOD_PROCESSOR', 'Food Processing Mill / Industry'
        INSTITUTIONAL = 'INSTITUTIONAL', 'Institutional / Corporate Buyer'
        RETAILER = 'RETAILER', 'Organized Retail / Supermarket'
        EXPORTER = 'EXPORTER', 'Agri Exporter'

    class VerificationLevel(models.IntegerChoices):
        LEVEL_1 = 1, 'Level 1: Phone Verified'
        LEVEL_2 = 2, 'Level 2: Business License / GST Verified'
        LEVEL_3 = 3, 'Level 3: Trade & Payment Track Verified'
        LEVEL_4 = 4, 'Level 4: FPO Certified Procurement Partner'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buyer_profile')
    business_name = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.WHOLESALER)
    gst_number = models.CharField(max_length=20, blank=True)
    mandi_license_number = models.CharField(max_length=50, blank=True)
    verification_level = models.IntegerField(choices=VerificationLevel.choices, default=VerificationLevel.LEVEL_1)
    is_verified = models.BooleanField(default=False)
    state = models.CharField(max_length=100, default='Haryana')
    district = models.CharField(max_length=100, default='Karnal')
    operating_mandi = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.business_name} ({self.get_category_display()}) - L{self.verification_level}"

class BuyerRequirement(models.Model):
    class PaymentTerms(models.TextChoices):
        IMMEDIATE = 'IMMEDIATE', 'Instant UPI / Direct Bank Transfer'
        SAME_DAY = 'SAME_DAY', 'Same Day Mandi Cleared Payment'
        DAYS_3 = 'DAYS_3', 'Within 3 Business Days'
        ON_DELIVERY = 'ON_DELIVERY', 'Upon Weighment & Moisture Check'

    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE, related_name='requirements')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    variety = models.ForeignKey(CropVariety, on_delete=models.SET_NULL, null=True, blank=True)
    quantity_required_quintals = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order_quintals = models.DecimalField(max_digits=10, decimal_places=2, default=5.0)
    offered_price_per_quintal = models.DecimalField(max_digits=10, decimal_places=2)
    quality_specifications = models.TextField(default="Max moisture 12%, foreign matter < 1%, zero discoloration.")
    delivery_point = models.CharField(max_length=200, default="Karnal New Grain Market Gate 2")
    payment_terms = models.CharField(max_length=20, choices=PaymentTerms.choices, default=PaymentTerms.SAME_DAY)
    valid_until = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer.business_name}: {self.crop.name} @ ₹{self.offered_price_per_quintal}/qtl"

class BuyerEnquiry(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = 'SUBMITTED', 'Enquiry Submitted'
        ACCEPTED = 'ACCEPTED', 'Accepted by Buyer'
        NEGOTIATING = 'NEGOTIATING', 'Price / Terms Counter-Offer'
        CONFIRMED = 'CONFIRMED', 'Confirmed Deal - Ready for Delivery'
        REJECTED = 'REJECTED', 'Closed / Declined'

    requirement = models.ForeignKey(BuyerRequirement, on_delete=models.CASCADE, related_name='enquiries')
    farmer = models.ForeignKey('farmers.FarmerProfile', on_delete=models.CASCADE, related_name='enquiries')
    offered_quantity_quintals = models.DecimalField(max_digits=10, decimal_places=2)
    expected_rate_per_quintal = models.DecimalField(max_digits=10, decimal_places=2)
    farmer_notes = models.TextField(blank=True)
    buyer_response = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Enquiry #{self.id}: {self.farmer.user.username} -> {self.requirement.buyer.business_name} ({self.status})"
