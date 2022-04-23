# Generated by Django 4.0.3 on 2022-04-12 10:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InsuranceCompany',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=10)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insurance_companies', to='tenants.tenant')),
            ],
            options={
                'db_table': 'Insurance Company',
            },
        ),
    ]
