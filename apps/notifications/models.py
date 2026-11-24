from django.db import models
from django.conf import settings

class Notification(models.Model):
    class Category(models.TextChoices):
        PRICE_ALERT = 'PRICE_ALERT', 'Mandi Price Movement Alert'
        BUYER_QUOTE = 'BUYER_QUOTE', 'Buyer Offer / Enquiry Update'
        SCHEME = 'SCHEME', 'Government Scheme Update / Deadline'
        DISEASE = 'DISEASE', 'Crop Health / Weather Advisory'
        SYSTEM = 'SYSTEM', 'Security & Account Notification'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.PRICE_ALERT)
    link_url = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.category}] {self.title} for {self.user.username}"
