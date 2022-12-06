from django.db import models
from artpage.models import ArtPiece
# Create your models here.

class ShippingAddress(models.Model):
    name = models.CharField(
        "Full name",
        max_length=1024,
    )

    address1 = models.CharField(
        "Address line 1",
        max_length=1024,
    )

    address2 = models.CharField(
        "Address line 2",
        max_length=1024,
    )

    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
    )

    city = models.CharField(
        "City",
        max_length=1024,
    )

    country = models.CharField(
        "Country",
        max_length=3,
    )

class Customer(models.Model):
    first_name = models.CharField(max_length=200, null=False)
    last_name = models.CharField(max_length=200, null=False)
    email = models.EmailField(null=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(ShippingAddress, on_delete=models.PROTECT)

    def __str__(self):
        return self.last_name

class Product(models.Model):
    TIER_1 = '1'
    TIER_2 = '2'
    TIER_3 = '3'
    TIER_4 = '4'
    TIER_5 = '5'
    PRODUCT_NAME_CHOICES = [
        (TIER_1, '1'),
        (TIER_2, '2'),
        (TIER_3, '3'),
        (TIER_4, '4'),
        (TIER_5, '5'),
    ]
    name = models.CharField(max_length=100, choices=PRODUCT_NAME_CHOICES, default=TIER_1)
    stripe_product_id = models.CharField(max_length=100)
    product_description = models.CharField(max_length=300, null=True)
    item = models.name = models.ForeignKey(ArtPiece, related_name='product_item', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prices")
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # dollars
    price_description = models.CharField(max_length=300, null=True)

    class Meta:
        ordering = ['price']
	
    def get_display_price(self):
        return "{0:.2f}".format(self.price)

    def __str__(self):
        return '%s %s %s %s' % ("$", self.price, "-", self.price_description)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Package Type: ')
    price = models.ForeignKey(Price, on_delete=models.CASCADE, verbose_name="Number of stems: ")
    shipping_address = models.FileField(upload_to='studio_orders/', verbose_name="Upload zipped music file: ")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cust_details')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default= False)
    customer_paid = models.FloatField(default= 0)
    stripe_order_id = models.CharField(max_length=100, null=True)
    fullfilment_date = models.DateTimeField(null=True)