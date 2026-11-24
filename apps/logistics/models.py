from django.db import models

class StorageFacility(models.Model):
    class FacilityType(models.TextChoices):
        WAREHOUSE = 'WAREHOUSE', 'Scientific Grain Warehouse (Godam)'
        COLD_STORAGE = 'COLD_STORAGE', 'Cold Storage (Sheetagrah) for Perishables'
        GRAIN_SILO = 'GRAIN_SILO', 'Steel Grain Silo'
        FPO_RURAL_STORAGE = 'RURAL_STORAGE', 'Village / FPO Storage Shed'

    name = models.CharField(max_length=200)
    facility_type = models.CharField(max_length=30, choices=FacilityType.choices, default=FacilityType.WAREHOUSE)
    state = models.CharField(max_length=100, default='Haryana')
    district = models.CharField(max_length=100, default='Karnal')
    location = models.CharField(max_length=250, default='GT Road, Industrial Area, Karnal')
    total_capacity_mt = models.DecimalField(max_digits=10, decimal_places=2, default=5000.0, help_text="Total Capacity in Metric Tonnes")
    available_capacity_mt = models.DecimalField(max_digits=10, decimal_places=2, default=1250.0)
    monthly_rate_per_quintal = models.DecimalField(max_digits=8, decimal_places=2, default=12.50, help_text="Rental charge in ₹/qtl/month")
    contact_phone = models.CharField(max_length=20, default='0184-2258900')
    is_wdra_accredited = models.BooleanField(default=True, verbose_name="WDRA Accredited (Eligible for e-NWR Loans)")

    def __str__(self):
        return f"{self.name} - {self.district} ({self.get_facility_type_display()})"

class Transporter(models.Model):
    class VehicleType(models.TextChoices):
        TRACTOR_TROLLEY = 'TRACTOR_TROLLEY', 'Tractor Trolley (4-6 Tonnes / 40-60 qtl)'
        PICKUP_TRUCK = 'PICKUP_TRUCK', 'Bolero Maxi Truck / Tata Ace (1.5-2.5 Tonnes / 15-25 qtl)'
        MEDIUM_TRUCK = 'MEDIUM_TRUCK', 'Eicher 6-Wheeler (7-10 Tonnes / 70-100 qtl)'
        HEAVY_TRUCK = 'HEAVY_TRUCK', '10-12 Wheeler Truck (16-25 Tonnes / 160-250 qtl)'

    transporter_name = models.CharField(max_length=150)
    vehicle_type = models.CharField(max_length=30, choices=VehicleType.choices, default=VehicleType.TRACTOR_TROLLEY)
    capacity_quintals = models.DecimalField(max_digits=8, decimal_places=2, default=50.0)
    rate_per_km = models.DecimalField(max_digits=8, decimal_places=2, default=35.0, help_text="Standard rate ₹ per km")
    base_loading_charge = models.DecimalField(max_digits=8, decimal_places=2, default=300.0)
    operating_district = models.CharField(max_length=100, default='Karnal')
    contact_phone = models.CharField(max_length=20, default='+91 98120 44556')
    is_verified = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.transporter_name} ({self.get_vehicle_type_display()}) - {self.operating_district}"
