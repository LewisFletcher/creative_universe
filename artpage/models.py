from django.db import models

# Managers

class CollectionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(name='No Collection')

class NoCollectionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(collection='1')

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

class Collection(models.Model):
    name= models.CharField(max_length=50)
    description= models.CharField(max_length=500)
    image= models.ImageField(blank=True, upload_to='collections/')
    last_updated= models.DateTimeField(auto_now=True)
    objects = models.Manager()
    all_collections = CollectionManager()

    def __str__(self):
        return self.name

class ArtPiece(models.Model):
   title= models.CharField(max_length=50)
   description= models.CharField(max_length=100)
   art_type= models.ForeignKey(ArtType, on_delete=models.CASCADE)
   canvas_size= models.CharField(max_length= 8, blank=True)
   image= models.ImageField(upload_to='artwork/')
   uploaded= models.DateField(auto_now_add=True)
   collection= models.ForeignKey(Collection, blank=True, on_delete=models.PROTECT, null=True)
   objects = models.Manager()
   no_collection = NoCollectionManager()
   creator= models.ForeignKey(Creator, on_delete=models.PROTECT, blank=True, null=True)
   landscape = models.BooleanField(default=False)

   def __str__(self):
        return self.title