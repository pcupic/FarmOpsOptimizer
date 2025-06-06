# Generated by Django 5.2 on 2025-04-10 20:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('CEREAL', 'Cereal'), ('LEGUME', 'Legume'), ('VEGETABLE', 'Vegetable'), ('FRUIT', 'Fruit'), ('TUBER', 'Tuber'), ('ROOT', 'Root'), ('LEAFY', 'Leafy'), ('NUT', 'Nut'), ('HERB', 'Herb'), ('FLOWER', 'Flower')], max_length=100)),
                ('sowing_time', models.CharField(choices=[('JANUARY', 'January'), ('FEBRUARY', 'February'), ('MARCH', 'March'), ('APRIL', 'April'), ('MAY', 'May'), ('JUNE', 'June'), ('JULY', 'July'), ('AUGUST', 'August'), ('SEPTEMBER', 'September'), ('OCTOBER', 'October'), ('NOVEMBER', 'November'), ('DECEMBER', 'December'), ('SPRING', 'Spring'), ('SUMMER', 'Summer'), ('AUTUMN', 'Autumn'), ('WINTER', 'Winter')], max_length=20)),
                ('harvesting_time', models.CharField(max_length=100)),
                ('optimal_conditions', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='FieldForm',
        ),
        migrations.RemoveField(
            model_name='field',
            name='crop_type',
        ),
        migrations.AddField(
            model_name='field',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='field_type',
            field=models.CharField(choices=[('GRAZING', 'Grazing'), ('PLANTING', 'Planting')], default='GRAZING', max_length=10),
        ),
        migrations.AddField(
            model_name='field',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='planting_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='field',
            name='soil_type',
            field=models.CharField(choices=[('LOAM', 'Loam'), ('CLAY', 'Clay'), ('SILT', 'Silt'), ('SAND', 'Sand'), ('PEAT', 'Peat')], default='LOAM', max_length=10),
        ),
        migrations.AlterField(
            model_name='field',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AddField(
            model_name='field',
            name='crop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crops.crop'),
        ),
    ]
