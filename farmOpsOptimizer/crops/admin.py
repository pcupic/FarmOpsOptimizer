from django.contrib import admin
from .models import PlantingField, GrazingField, Crop, PlantingReport, HarvestSummary

admin.site.register(GrazingField)
admin.site.register(PlantingField)
admin.site.register(Crop)
admin.site.register(PlantingReport)
admin.site.register(HarvestSummary)
