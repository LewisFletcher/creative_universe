# Generated by Django 4.2.10 on 2024-03-19 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artpage', '0014_collection_long_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artpiece',
            name='description',
        ),
        migrations.RemoveField(
            model_name='merch',
            name='description',
        ),
        migrations.RemoveField(
            model_name='photographyprints',
            name='description',
        ),
        migrations.RemoveField(
            model_name='print',
            name='description',
        ),
        migrations.RemoveField(
            model_name='sticker',
            name='description',
        ),
    ]