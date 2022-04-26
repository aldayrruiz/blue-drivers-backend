# Generated by Django 4.0.3 on 2022-04-12 10:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vehicles', '0001_initial'),
        ('tenants', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recurrent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('weekdays', models.CharField(max_length=13)),
                ('since', models.DateTimeField()),
                ('until', models.DateTimeField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recurrences', to=settings.AUTH_USER_MODEL)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recurrences', to='tenants.tenant')),
            ],
            options={
                'db_table': 'Recurrent',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('date_stored', models.DateField(auto_now_add=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('description', models.TextField(blank=True, default='')),
                ('is_cancelled', models.BooleanField(default=False)),
                ('is_recurrent', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL)),
                ('recurrent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='reservations.recurrent')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='tenants.tenant')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='vehicles.vehicle')),
            ],
            options={
                'db_table': 'Reservation',
                'ordering': ['-start'],
            },
        ),
    ]