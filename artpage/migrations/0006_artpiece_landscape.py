# Generated by Django 4.1.3 on 2024-01-28 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artpage', '0005_artpiece_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='artpiece',
            name='landscape',
            field=models.BooleanField(default=False),
        ),
    ]