# Generated by Django 4.1.7 on 2023-05-21 15:00

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0009_vehicle_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='icon',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, null=True, quality=100, scale=None, size=[750, 750], upload_to='vehicles/icons'),
        ),
    ]
