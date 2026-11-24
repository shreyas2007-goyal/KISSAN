from django.db import models
from django.conf import settings

class UserAccessibilityPreference(models.Model):
    class ThemeMode(models.TextChoices):
        LIGHT = 'light', 'Standard Light Mode'
        DARK = 'dark', 'Comfort Dark Mode'
        HIGH_CONTRAST = 'high-contrast', 'High Contrast Black & Yellow Mode'

    class TextSize(models.TextChoices):
        NORMAL = 'normal', 'Standard Text (100%)'
        LARGE = 'large', 'Large Text (125%)'
        EXTRA_LARGE = 'xlarge', 'Jumbo Text (150%)'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accessibility_pref', null=True, blank=True)
    theme_mode = models.CharField(max_length=20, choices=ThemeMode.choices, default=ThemeMode.LIGHT)
    text_size = models.CharField(max_length=20, choices=TextSize.choices, default=TextSize.NORMAL)
    simple_farmer_mode = models.BooleanField(default=False, help_text="Streamlined interface with simplified cards and larger touch targets")
    voice_assistance = models.BooleanField(default=True, help_text="Enable voice readouts and voice query prompts")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        user_label = self.user.username if self.user else "Anonymous / Session"
        return f"A11y: {user_label} ({self.theme_mode}, {self.text_size}, Simple={self.simple_farmer_mode})"
