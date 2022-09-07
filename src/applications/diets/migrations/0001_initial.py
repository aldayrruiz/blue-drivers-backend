# Generated by Django 4.0.5 on 2022-08-22 10:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reservations', '0002_reservation_incidents'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tenants', '0003_tenant_diet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('Gasolina', 'Gasolina'), ('Parking', 'Parking'), ('Peaje', 'Peaje'), ('Alojamiento', 'Alojamiento'), ('Otros', 'Otros')], default='Otros', max_length=20)),
                ('liters', models.IntegerField(blank=True, default=-1)),
                ('amount', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, default='')),
            ],
            options={
                'db_table': 'Diet',
            },
        ),
        migrations.CreateModel(
            name='DietPhoto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('photo', models.ImageField(default='diet/none.png', upload_to='diets')),
                ('diet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='diets.diet')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diet_photos', to=settings.AUTH_USER_MODEL)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenants.tenant')),
            ],
            options={
                'db_table': 'DietPhoto',
            },
        ),
        migrations.CreateModel(
            name='DietCollection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('completed', models.BooleanField(default=False)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('date_stored', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diet_collections', to=settings.AUTH_USER_MODEL)),
                ('reservation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='diet_collection', to='reservations.reservation')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenants.tenant')),
            ],
            options={
                'db_table': 'DietCollection',
            },
        ),
        migrations.AddField(
            model_name='diet',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diets', to='diets.dietcollection'),
        ),
        migrations.AddField(
            model_name='diet',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='diet',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diets', to='tenants.tenant'),
        ),
    ]
