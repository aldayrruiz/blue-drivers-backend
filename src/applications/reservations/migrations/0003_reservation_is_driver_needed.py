# Generated by Django 4.0.5 on 2022-09-26 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_reservation_incidents'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='is_driver_needed',
            field=models.BooleanField(default=False),
        ),
    ]
