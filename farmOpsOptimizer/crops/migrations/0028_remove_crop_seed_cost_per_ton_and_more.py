# Generated by Django 5.2 on 2025-04-19 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crops', '0027_seedpurchase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crop',
            name='seed_cost_per_ton',
        ),
        migrations.RemoveField(
            model_name='crop',
            name='seed_quantity_in_tons',
        ),
        migrations.DeleteModel(
            name='SeedPurchase',
        ),
    ]
