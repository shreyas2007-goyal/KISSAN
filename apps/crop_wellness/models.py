from django.db import models
from apps.crops.models import Crop

class DiseaseProfile(models.Model):
    class Severity(models.TextChoices):
        LOW = 'LOW', 'Low - Early Stage Actionable'
        MODERATE = 'MODERATE', 'Moderate - Treatment Required'
        SEVERE = 'SEVERE', 'Severe - Urgent Intervention'
        BENIGN = 'BENIGN', 'Healthy / Non-Pathogenic'

    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='diseases')
    name_en = models.CharField(max_length=150)
    name_hi = models.CharField(max_length=150, blank=True)
    name_pa = models.CharField(max_length=150, blank=True)
    causal_agent = models.CharField(max_length=150, default='Fungal / Bacterial Pathogen')
    symptoms = models.TextField()
    symptoms_hi = models.TextField(blank=True)
    treatment = models.TextField()
    treatment_hi = models.TextField(blank=True)
    preventive_measures = models.TextField()
    recommended_pesticide = models.CharField(max_length=200, blank=True, help_text="Authoritative agricultural university recommended fungicide/insecticide formulation")
    default_severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.MODERATE)

    def __str__(self):
        return f"{self.crop.name} - {self.name_en} ({self.name_hi})"

class CropHealthAnalysis(models.Model):
    class SeverityGrade(models.TextChoices):
        HEALTHY = 'HEALTHY', 'Healthy Crop'
        LOW = 'LOW', 'Mild Symptoms (Stage 1)'
        MODERATE = 'MODERATE', 'Moderate Infection (Stage 2)'
        SEVERE = 'SEVERE', 'Critical / Advanced Spread (Stage 3)'
        UNCERTAIN = 'UNCERTAIN', 'Inconclusive / Low Confidence'

    farmer = models.ForeignKey('farmers.FarmerProfile', on_delete=models.CASCADE, null=True, blank=True, related_name='crop_screenings')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='crop_images/')
    model_version = models.CharField(max_length=50, default='KisanVision-PyTorch-v2.1')
    predicted_disease = models.ForeignKey(DiseaseProfile, on_delete=models.SET_NULL, null=True, blank=True)
    confidence_score = models.FloatField(default=0.0)
    severity = models.CharField(max_length=20, choices=SeverityGrade.choices, default=SeverityGrade.MODERATE)
    is_healthy = models.BooleanField(default=False)
    expert_consultation_recommended = models.BooleanField(default=True)
    disclaimer = models.TextField(
        default="This is an automated preliminary AI screening result, not a certified laboratory diagnosis. For severe crop distress, verify with your local Krishi Vigyan Kendra (KVK) officer."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        disease_name = self.predicted_disease.name_en if self.predicted_disease else "Healthy / Unknown"
        return f"Analysis #{self.id}: {self.crop.name} - {disease_name} ({self.confidence_score*100:.1f}%)"
