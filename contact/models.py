from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    order_number = models.CharField(max_length=32, null=True, blank=True, help_text="If you have an order number, please enter it here.")
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'