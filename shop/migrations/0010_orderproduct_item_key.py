# Generated by Django 4.2.10 on 2024-02-20 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_remove_order_customer_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='item_key',
            field=models.CharField(max_length=100, null=True),
        ),
    ]