from django.db import models
from django.contrib.auth.models import User 

class Crop(models.Model):
    CROP_TYPES = [
        ('CEREAL', 'Cereal'),
        ('LEGUME', 'Legume'),
        ('VEGETABLE', 'Vegetable'),
        ('FRUIT', 'Fruit'),
        ('TUBER', 'Tuber'),
        ('ROOT', 'Root'),
        ('LEAFY', 'Leafy'),
        ('NUT', 'Nut'),
        ('HERB', 'Herb'),
        ('FLOWER', 'Flower'),
    ]
    
    SOWING_TIMES = [
        ('JANUARY', 'January'),
        ('FEBRUARY', 'February'),
        ('MARCH', 'March'),
        ('APRIL', 'April'),
        ('MAY', 'May'),
        ('JUNE', 'June'),
        ('JULY', 'July'),
        ('AUGUST', 'August'),
        ('SEPTEMBER', 'September'),
        ('OCTOBER', 'October'),
        ('NOVEMBER', 'November'),
        ('DECEMBER', 'December'),
        ('SPRING', 'Spring'),
        ('SUMMER', 'Summer'),
        ('AUTUMN', 'Autumn'),
        ('WINTER', 'Winter'),
    ]
    
    VARIETY_TYPES = [
        ('HYBRID', 'Hybrid'),
        ('OPEN_POLLINATED', 'Open Pollinated'),
        ('EARLY', 'Early Maturing'),
        ('LATE', 'Late Maturing'),
        ('DROUGHT_TOLERANT', 'Drought Tolerant'),
        ('DISEASE_RESISTANT', 'Disease Resistant'),
        ('HIGH_YIELD', 'High Yield'),
        ('SILAGE', 'Silage'),
        ('GRAIN', 'Grain'),
        ('FODDER', 'Fodder'),
        ('ORGANIC', 'Organic'),
        ('CONVENTIONAL', 'Conventional'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=CROP_TYPES)
    sowing_time = models.CharField(max_length=20, choices=SOWING_TIMES)  
    harvesting_time_start = models.DateTimeField(null=True, blank=True)  
    harvesting_time_end = models.DateTimeField(null=True, blank=True)  
    optimal_conditions = models.TextField()
    botanical_name = models.CharField(max_length=200, blank=True, null=True) 
    row_spacing = models.FloatField(null=True, blank=True)  
    planting_depth = models.FloatField(null=True, blank=True)  
    average_height = models.FloatField(null=True, blank=True) 
    plant_spacing = models.FloatField(null=True, blank=True)  
    days_to_emerge = models.IntegerField(null=True, blank=True) 
    days_to_flower = models.IntegerField(null=True, blank=True) 
    days_to_maturity = models.IntegerField(null=True, blank=True)  
    estimated_revenue_per_harvest_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
    estimated_yield_per_ha = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    manufacturer = models.CharField(max_length=100, null=True, blank=True)
    variety_type = models.CharField(max_length=100, choices=VARIETY_TYPES, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class PlantingField(models.Model):
    SOIL_TYPES = [
        ('LOAM', 'Loam'),
        ('CLAY', 'Clay'),
        ('SILT', 'Silt'),
        ('SAND', 'Sand'),
        ('PEAT', 'Peat'),
    ]

    LIGHT_PROFILES = [
        ('FULL_SUN', 'Full Sun'),
        ('PARTIAL_SHADE', 'Partial Shade'),
        ('FULL_SHADE', 'Full Shade'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  
    name = models.CharField(max_length=100)
    area = models.FloatField()  
    soil_type = models.CharField(max_length=10, choices=SOIL_TYPES, default='LOAM') 
    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, blank=True) 
    planting_date = models.DateTimeField(null=True, blank=True)
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    light_profile = models.CharField(max_length=15, choices=LIGHT_PROFILES, null=True, blank=True)

    def __str__(self):
        return self.name
    
class GrazingField(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  
    name = models.CharField(max_length=100)
    area = models.FloatField() 
    grazing_rest_days = models.PositiveIntegerField(null=True, blank=True, help_text="Rest days after grazing before reuse")
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    water_source = models.CharField(max_length=50, blank=True, null=True) 
    
class PlantingReport(models.Model):
    planting_field = models.ForeignKey(PlantingField, on_delete=models.CASCADE, related_name="reports")
    report_date = models.DateTimeField(auto_now_add=True)  
    plant_height = models.FloatField(null=True, blank=True)  
    plant_health = models.CharField(max_length=255, blank=True, null=True) 
    
    FLOWERING_STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('BEGINNING', 'Beginning of Flowering'),
        ('PEAK', 'Full Flowering'),
        ('ENDING', 'End of Flowering'),
        ('COMPLETED', 'Flowering Completed'),
    ]
    flowering_status = models.CharField(max_length=50, choices=FLOWERING_STATUS_CHOICES, default='NOT_STARTED')
    
    MATURITY_STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('BEGINNING', 'Beginning of Maturity'),
        ('HALFWAY', 'Halfway to Maturity'),
        ('NEAR_COMPLETION', 'Near Completion'),
        ('COMPLETED', 'Fully Matured'),
    ]
    maturity_status = models.CharField(max_length=50, choices=MATURITY_STATUS_CHOICES, default='NOT_STARTED')
    
    temperature = models.FloatField(null=True, blank=True)  
    humidity = models.FloatField(null=True, blank=True) 
    notes = models.TextField(blank=True, null=True)  
    archived = models.BooleanField(default=False)  

    def __str__(self):
        return f"Report for {self.planting_field.name} on {self.report_date}"
    
class HarvestSummary(models.Model):
    field = models.ForeignKey(PlantingField, on_delete=models.CASCADE, related_name='harvest_summaries')
    season = models.CharField(max_length=20)
    yield_in_tons = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_ton = models.DecimalField(max_digits=10, decimal_places=2)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.yield_in_tons and self.price_per_ton:
            self.total_revenue = self.yield_in_tons * self.price_per_ton
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Harvest Summary for {self.field.name} ({self.season})"
