from django.db import models
from django.core.validators import MinLengthValidator
from artpage.models import ArtPiece
from markdownx.models import MarkdownxField

# Create your models here.

class Katelyn(models.Model):
    info = MarkdownxField(help_text='Enter everything you want to say here. You can use markdown to format your text: https://www.markdownguide.org/basic-syntax/', null=True, blank=True)

    def __str__(self):
        return str(self.pk)