from django.contrib import admin
from .models import ArtType, ArtPiece, Collection
# Register your models here.

admin.site.register(ArtType)
admin.site.register(ArtPiece)
admin.site.register(Collection)