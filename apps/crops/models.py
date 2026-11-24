from django.db import models

class Crop(models.Model):
    class Category(models.TextChoices):
        CEREAL = 'CEREAL', 'Cereal / Anaj'
        PULSE = 'PULSE', 'Pulse / Dal'
        OILSEED = 'OILSEED', 'Oilseed / Tilhan'
        VEGETABLE = 'VEGETABLE', 'Vegetable / Sabzi'
        CASH_CROP = 'CASH_CROP', 'Cash Crop / Vyavasayik'
        FRUIT = 'FRUIT', 'Fruit / Phal'

    name = models.CharField(max_length=100, unique=True)
    name_hi = models.CharField(max_length=100, blank=True)
    name_pa = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.CEREAL)
    standard_msp_quintal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Minimum Support Price (MSP) per Quintal")
    typical_growing_days = models.PositiveIntegerField(default=120)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.name_hi or ''})"

class CropVariety(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='varieties')
    variety_name = models.CharField(max_length=100)
    maturity_days = models.PositiveIntegerField(default=120)
    ideal_soil = models.CharField(max_length=100, blank=True)
    characteristics = models.TextField(blank=True)

    def __str__(self):
        return f"{self.crop.name} - {self.variety_name}"
