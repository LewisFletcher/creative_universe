from django.db import models
from itertools import chain
from operator import attrgetter
from django.db.models import Q

# Managers

class CollectionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(name='No Collection')

class NoCollectionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(collection='1')
    
class CommonModelMixin:
    def get_model_name(self):
        return self.__class__.__name__

    def in_stock(self):
        if self.total_stock is None:
            return True
        elif self.total_stock > 0:
            return True
        else:
            return False

    def second_image(self):
        if self.extra_images.all().exists():
            return self.extra_images.all()[0]
        return None

# Models

class Creator(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ArtType(models.Model):
    name= models.CharField(max_length=50)
    desciption= models.CharField(max_length=200)
    required_stationary= models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name
    
class ExtraImages(models.Model):
    image= models.ImageField(upload_to='extra_images/')


    def __str__(self):
        return self.image.url

class Collection(models.Model):
    name= models.CharField(max_length=50)
    description= models.CharField(max_length=100)
    long_description = models.TextField(blank=True, null=True, max_length=670)
    image= models.ImageField(blank=True, upload_to='collections/')
    last_updated= models.DateTimeField(auto_now=True)
    objects = models.Manager()
    is_collection = models.BooleanField(default=True)
    all_collections = CollectionManager()

    def second_image(self):
        if self.artpiece_set.all().count() > 0:
            return self.artpiece_set.all()[0].image
        else:
            return None

    def __str__(self):
        return self.name

class ArtPiece(models.Model):
    title= models.CharField(max_length=50)
    long_description = models.TextField(blank=True, null=True, max_length=670)
    total_stock = models.IntegerField(null=True, blank=True)
    art_type= models.ForeignKey(ArtType, on_delete=models.CASCADE)
    canvas_size= models.CharField(max_length= 8, blank=True)
    image= models.ImageField(upload_to='artwork/')
    extra_images = models.ManyToManyField(ExtraImages, blank=True)
    uploaded= models.DateField(auto_now_add=True)
    collection= models.ForeignKey(Collection, blank=True, on_delete=models.PROTECT, null=True)
    product = models.ForeignKey('shop.Product', on_delete=models.PROTECT, blank=True, null=True)
    objects = models.Manager()
    no_collection = NoCollectionManager()
    creator= models.ForeignKey(Creator, on_delete=models.PROTECT, blank=True, null=True)

    def get_model_name(self):
        return self.__class__.__name__
    
    def in_stock(self):
        if self.total_stock is None:
            return True
        elif self.total_stock > 0:
            return True
        else:
            return False
        
    def second_image(self):
        if self.extra_images.all().count() > 0:
            print(self.extra_images.all()[0])
            return self.extra_images.all()[0]
        else:
            return None
        
    def detail_url(self):
        return '/portfolio/art/details/' + str(self.id)

    def __str__(self):
        return self.title
    
class Print(CommonModelMixin, models.Model):
    title= models.CharField(max_length=50)
    long_description = models.TextField(blank=True, null=True, max_length=670)
    total_stock = models.IntegerField(null=True, blank=True)
    art_type= models.ForeignKey(ArtType, on_delete=models.CASCADE)
    canvas_size= models.CharField(max_length= 8, blank=True)
    image= models.ImageField(upload_to='prints/')
    extra_images = models.ManyToManyField(ExtraImages, blank=True)
    product = models.ForeignKey('shop.Product', on_delete=models.PROTECT, blank=True, null=True)
    original= models.ForeignKey(ArtPiece, on_delete=models.PROTECT, blank=True, null=True)
    uploaded= models.DateField(auto_now_add=True)
    creator= models.ForeignKey(Creator, on_delete=models.PROTECT, blank=True, null=True)

    def detail_url(self):
        return '/shop/prints/details/' + str(self.id)

    def __str__(self):
        return self.title
    
class Sticker(CommonModelMixin, models.Model):
    title= models.CharField(max_length=50)
    long_description = models.TextField(blank=True, null=True, max_length=670)
    total_stock = models.IntegerField(null=True, blank=True)
    sticker_type= models.ForeignKey(ArtType, on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.PROTECT, blank=True, null=True)
    image= models.ImageField(upload_to='stickers/')
    extra_images = models.ManyToManyField(ExtraImages, blank=True)
    uploaded= models.DateField(auto_now_add=True)
    creator= models.ForeignKey(Creator, on_delete=models.PROTECT, blank=True, null=True)

    def detail_url(self):
        return '/shop/stickers/details/' + str(self.id)

    def __str__(self):
        return self.title
    
class PhotographyPrints(CommonModelMixin, models.Model):
    title= models.CharField(max_length=50)
    long_description = models.TextField(blank=True, null=True, max_length=670)
    total_stock = models.IntegerField(null=True, blank=True)
    product = models.ForeignKey('shop.Product', on_delete=models.PROTECT, blank=True, null=True)
    image= models.ImageField(upload_to='photography/')
    extra_images = models.ManyToManyField(ExtraImages, blank=True)
    uploaded= models.DateField(auto_now_add=True)
    creator= models.ForeignKey(Creator, on_delete=models.PROTECT, blank=True, null=True)

    def detail_url(self):
        return '/shop/photography-prints/details/' + str(self.id)

    def __str__(self):
        return self.title
    
class Merch(CommonModelMixin, models.Model):
    title= models.CharField(max_length=50)
    long_description = models.TextField(blank=True, null=True, max_length=670)
    total_stock = models.IntegerField(null=True, blank=True)
    product = models.ForeignKey('shop.Product', on_delete=models.PROTECT, blank=True, null=True)
    image= models.ImageField(upload_to='merch/')
    extra_images = models.ManyToManyField(ExtraImages, blank=True)
    uploaded= models.DateField(auto_now_add=True)
    creator= models.ForeignKey(Creator, on_delete=models.PROTECT, blank=True, null=True)

    def detail_url(self):
        return '/shop/merch/details/' + str(self.id)

    def __str__(self):
        return self.title