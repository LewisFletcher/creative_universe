from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Katelyn(models.Model):
    full_name = models.CharField(max_length=100)
    art_style = models.TextField(
        validators=[MinLengthValidator(100, "Must be at least one hundred characters.")]
    )
    creative_universe_exp = models.TextField(
        validators=[MinLengthValidator(100, "Must be at least one hundred characters.")]
    )
    life = models.TextField(
        validators=[MinLengthValidator(100, "Must be at least one hundred characters.")]
    )
    selfie = models.ImageField(upload_to='about/', blank=True)
    favorite_art = models.ImageField(upload_to='about/', blank=True)
    favorite_art_reason = models.ImageField(upload_to='about/', blank=True)
    
    def __str__(self):
        return self.full_name