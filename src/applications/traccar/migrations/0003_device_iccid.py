# Generated by Django 4.1.7 on 2023-06-22 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traccar', '0002_device_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='iccid',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]
