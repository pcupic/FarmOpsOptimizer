from django.contrib import admin
from .models import Livestock, HealthRecord, VaccinationRecord, Species, Herd

admin.site.register(Livestock)
admin.site.register(HealthRecord)
admin.site.register(VaccinationRecord)
admin.site.register(Species)
admin.site.register(Herd)
