from django.db import models

# Create your models here.


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

   def __str__(self):
        return self.title