# Generated by Django 4.1.2 on 2022-11-11 09:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('diets', '0004_dietmonthlypdfreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='dietmonthlypdfreport',
            name='date_stored',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dietpayment',
            name='date_stored',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dietphoto',
            name='date_stored',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
