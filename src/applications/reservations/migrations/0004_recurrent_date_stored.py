# Generated by Django 4.1.2 on 2022-11-11 09:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_reservation_is_driver_needed'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurrent',
            name='date_stored',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]