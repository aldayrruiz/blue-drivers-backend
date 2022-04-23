# Generated by Django 4.0.3 on 2022-04-12 10:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('insurance_companies', '0001_initial'),
        ('traccar', '0001_initial'),
        ('tenants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('model', models.CharField(max_length=50)),
                ('brand', models.CharField(max_length=20)),
                ('number_plate', models.CharField(max_length=7, unique=True, validators=[django.core.validators.MinLengthValidator(7)])),
                ('date_stored', models.DateField(auto_now_add=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('fuel', models.CharField(choices=[('DIESEL', 'Diesel'), ('GASOLINE', 'Gasoline'), ('ELECTRIC', 'Electric')], default='DIESEL', max_length=10)),
                ('policy_number', models.CharField(blank=True, default='', max_length=20)),
                ('gps_device', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='traccar.device')),
                ('insurance_company', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='vehicles', to='insurance_companies.insurancecompany')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='tenants.tenant')),
            ],
            options={
                'db_table': 'Vehicle',
            },
        ),
    ]
