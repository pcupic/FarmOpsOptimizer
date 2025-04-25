from django.contrib import admin
from .models import Equipment, Seed, Feed, Fertilizer, Pesticide, SeedUsage, MaintenanceRecord, FertilizerUsage, PesticideUsage, FeedReport

admin.site.register(Equipment)
admin.site.register(Seed)
admin.site.register(Feed)
admin.site.register(Fertilizer)
admin.site.register(Pesticide)
admin.site.register(SeedUsage)
admin.site.register(MaintenanceRecord)
admin.site.register(FertilizerUsage)
admin.site.register(PesticideUsage)
admin.site.register(FeedReport)


