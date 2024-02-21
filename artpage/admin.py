from django.contrib import admin
from .models import ArtType, ArtPiece, Collection, Creator, Print, Sticker, ExtraImages, PhotographyPrints, Merch
# Register your models here.


admin.site.register(ArtType)
admin.site.register(ArtPiece)
admin.site.register(Collection)
admin.site.register(Creator)
admin.site.register(Print)
admin.site.register(Sticker)
admin.site.register(PhotographyPrints)
admin.site.register(Merch)
admin.site.register(ExtraImages)