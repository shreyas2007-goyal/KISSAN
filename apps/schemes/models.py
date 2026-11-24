from django.db import models

class Scheme(models.Model):
    class Level(models.TextChoices):
        CENTRAL = 'CENTRAL', 'Central Government Scheme (Kendra Sarkar)'
        STATE = 'STATE', 'State Government Scheme (Rajya Sarkar)'

    name = models.CharField(max_length=200)
    name_hi = models.CharField(max_length=200, blank=True)
    name_pa = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=200, default='Ministry of Agriculture & Farmers Welfare')
    level = models.CharField(max_length=20, choices=Level.choices, default=Level.CENTRAL)
    applicable_state = models.CharField(max_length=100, default='All India')
    objective = models.TextField()
    objective_hi = models.TextField(blank=True)
    benefits = models.TextField()
    benefits_hi = models.TextField(blank=True)
    eligibility_criteria = models.TextField()
    eligibility_criteria_hi = models.TextField(blank=True)
    required_documents = models.TextField(default="Aadhaar Card, Land Revenue Records (Khasra/Khatauni), Bank Passbook, Mobile Number")
    official_portal_url = models.URLField(max_length=500)
    helpline_number = models.CharField(max_length=100, default='155261 / 011-24300606')
    last_verified_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.applicable_state})"

class SchemeBookmark(models.Model):
    farmer = models.ForeignKey('farmers.FarmerProfile', on_delete=models.CASCADE, related_name='bookmarked_schemes')
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name='bookmarks')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('farmer', 'scheme')

    def __str__(self):
        return f"{self.farmer.user.username} -> {self.scheme.name}"
