# Generated by Django 4.0.5 on 2022-10-05 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0004_vehicle_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='type',
            field=models.CharField(choices=[('TOURISM', 'Turismo'), ('ALL_TERRAIN', 'Todo terreno'), ('MOTORCYCLE', 'Motocicleta'), ('VAN', 'Furgoneta'), ('TRUCK', 'Camión')], default='TOURISM', max_length=20),
        ),
    ]