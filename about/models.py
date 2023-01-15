from django.db import models
from django.core.validators import MinLengthValidator
from artpage.models import ArtPiece

# Create your models here.

class Katelyn(models.Model):
    full_name = models.CharField(max_length=100)
    art_style = models.TextField(
        validators=[MinLengthValidator(100, "Must be at least one hundred characters.")]
    )
    creative_universe_exp = models.TextField(
        null=True,
        validators=[MinLengthValidator(100, "Must be at least one hundred characters.")]
    )
    life_info = models.TextField(
        null=True,
        validators=[MinLengthValidator(100, "Must be at least one hundred characters.")]
    )
    selfie = models.ImageField(upload_to='about/', blank=True)
    favorite_art_piece = models.ForeignKey(ArtPiece, on_delete=models.SET_NULL, blank=True, null=True)
    favorite_art_reason = models.TextField(
        null=True,
        validators=[MinLengthValidator(50, "Must be at least one fifty characters.")]
    )
    biography_1 = models.TextField(
        null=True,
        validators=[MinLengthValidator(100, "Must be at least one hundred characters.")]
    )
    biography_2 = models.TextField(
        null=True,
        validators=[MinLengthValidator(100, "Must be at least one hundred characters.")]
    )
    biography_3 = models.TextField(
        null=True,
        validators=[MinLengthValidator(100, "Must be at least one hundred characters.")]
    )
    biography_4 = models.TextField(
        null=True,
        validators=[MinLengthValidator(100, "Must be at least one hundred characters.")]
    )
    contact_email = models.EmailField(null=True,)
    places_lived = models.TextField(
        null=True,
        validators=[MinLengthValidator(20, "Must be at least one twenty characters.")]
    )
    age = models.IntegerField(null=True,)


    
    def __str__(self):
        return self.full_name