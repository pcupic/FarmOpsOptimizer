# Generated by Django 5.2 on 2025-04-18 14:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crops', '0019_remove_harvestsummary_archived_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='plantingfield',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='PlantingFieldTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('notes', models.TextField(blank=True, null=True)),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchased_fields', to=settings.AUTH_USER_MODEL)),
                ('planting_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='crops.plantingfield')),
            ],
        ),
    ]
