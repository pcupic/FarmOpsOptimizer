# Generated by Django 5.1.2 on 2025-05-03 17:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crops', '0029_remove_plantingfieldtransaction_buyer_and_more'),
        ('resources', '0024_equipment_condition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pesticideusage',
            name='field',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='crops.plantingfield'),
            preserve_default=False,
        ),
    ]
