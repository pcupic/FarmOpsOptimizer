from django.db import models
from crops.models import PlantingField, Crop, GrazingField
from django.contrib.auth.models import User

class Equipment(models.Model):
    condition_choices = [
        ('NEW', 'New'),
        ('USED', 'Used'),
        ('BROKEN', 'Broken'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  
    name = models.CharField(max_length=100, null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_maintenance_date = models.DateTimeField(null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    condition = models.CharField(
        max_length=6, 
        choices=condition_choices, 
        default='NEW', 
    )
    
    def __str__(self):
        return f"Equipment: {self.name}"

class MaintenanceRecord(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='maintenance_records')
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Maintenance for {self.equipment.name} on {self.date.strftime('%Y-%m-%d')}"

class Seed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  

    unit_of_measure = models.CharField(
        max_length=20,
        choices=[
            ('KG', 'Kilogram'),
            ('G', 'Gram'),
            ('L', 'Litre'),
            ('ML', 'Millilitre'),
            ('UNIT', 'Unit/Piece'),
            ('TON', 'Tonne'),
            ('BAG', 'Bag'),
            ('BOX', 'Box'),
            ('PACK', 'Pack'),
            ('SACK', 'Sack'),
            ('TRAY', 'Tray'),
            ('BOTTLE', 'Bottle'),
            ('BARREL', 'Barrel'),
            ('HECTOLITRE', 'Hectolitre'),
            ('M3', 'Cubic meter'),
            ('OTHER', 'Other'),
        ],
        default='UNIT'
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    crop = models.OneToOneField(Crop, on_delete=models.CASCADE, null=True, blank=True)
    sowing_instructions = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Seed: {self.name} - {self.crop}"

class SeedUsage(models.Model):
    field = models.ForeignKey(PlantingField, on_delete=models.CASCADE)
    seed = models.ForeignKey(Seed, on_delete=models.CASCADE)
    quantity_used = models.FloatField(null=True, blank=True)
    usage_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity_used} units of {self.seed.name} used on {self.field.name}"

class Fertilizer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  

    FERTILIZER_TYPES = [
        ('NITROGEN', 'Nitrogen-based'),
        ('PHOSPHORUS', 'Phosphorus-based'),
        ('POTASSIUM', 'Potassium-based'),
        ('COMPOSITE', 'Composite'),
        ('LIQUID', 'Liquid'),
        ('ORGANIC', 'Organic'),
        ('INORGANIC', 'Inorganic'),
        ('BIOLOGICAL', 'Biological'),
        ('SLOW_RELEASE', 'Slow-release'),
        ('MINERAL', 'Mineral-based'),
        ('COMPOST', 'Compost'),
        ('FOLIAR', 'Foliar'),
        ('MICRONUTRIENT', 'Micronutrient'),
        ('LIQUID_FERTILIZER', 'Liquid Fertilizer'),
        ('OTHER', 'Other'),
    ]
    
    unit_of_measure = models.CharField(
        max_length=20,
        choices=[
            ('L', 'Litre'),
            ('ML', 'Millilitre'),
            ('UNIT', 'Unit/Piece'),
            ('BOTTLE', 'Bottle'),
            ('HECTOLITRE', 'Hectolitre'),
            ('M3', 'Cubic meter'),
            ('OTHER', 'Other'),
        ],
        default='UNIT'
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fertilizer_type = models.CharField(
        max_length=100,
        choices=FERTILIZER_TYPES,
        default='OTHER'
    )
    application_instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Fertilizer: {self.name} - {self.fertilizer_type}"

class FertilizerUsage(models.Model):
    fertilizer = models.ForeignKey(Fertilizer, on_delete=models.CASCADE, related_name='usages')
    field = models.ForeignKey(PlantingField, on_delete=models.SET_NULL, null=True, blank=True) 
    date_applied = models.DateTimeField(auto_now_add=True)
    amount_used = models.FloatField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.fertilizer.name} used on {self.field.name} on {self.date_applied}"

class Feed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    unit_of_measure = models.CharField(
        max_length=20,
        choices=[
            ('KG', 'Kilogram'),
            ('G', 'Gram'),
            ('UNIT', 'Unit/Piece'),
            ('TON', 'Tonne'),
            ('BAG', 'Bag'),
            ('BOX', 'Box'),
            ('PACK', 'Pack'),
            ('OTHER', 'Other'),
        ],
        default='UNIT'
    )
    name = models.CharField(max_length=100)
    quantity = models.FloatField(null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    feeding_instructions = models.TextField(blank=True, null=True)

    food_type = models.CharField(
        max_length=50,
        choices=[
            ('GRASS', 'Grass'),
            ('HAY', 'Hay'),
            ('GRAINS', 'Grains'),
            ('VEGETABLES', 'Vegetables'),
            ('FRUITS', 'Fruits'),
            ('SEEDS', 'Seeds'),
            ('FISHMEAL', 'Fishmeal'),
            ('OTHER', 'Other'),
        ],
        default='GRASS'
    )

    def __str__(self):
        return f"Feed: {self.name} - {self.food_type}"


class Pesticide(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  

    PESTICIDE_TYPES = [
        ('INSECTICIDE', 'Insecticide'),
        ('HERBICIDE', 'Herbicide'),
        ('FUNGICIDE', 'Fungicide'),
        ('RODENTICIDE', 'Rodenticide'),
        ('BACTERICIDE', 'Bactericide'),
        ('NEMATICIDE', 'Nematicide'),
        ('ACARICIDE', 'Acaricide'),
    ]
    
    unit_of_measure = models.CharField(
        max_length=20,
        choices=[
            ('KG', 'Kilogram'),
            ('G', 'Gram'),
            ('L', 'Litre'),
            ('ML', 'Millilitre'),
            ('UNIT', 'Unit/Piece'),
            ('TON', 'Tonne'),
            ('BAG', 'Bag'),
            ('BOX', 'Box'),
            ('PACK', 'Pack'),
            ('SACK', 'Sack'),
            ('TRAY', 'Tray'),
            ('BOTTLE', 'Bottle'),
            ('BARREL', 'Barrel'),
            ('HECTOLITRE', 'Hectolitre'),
            ('M3', 'Cubic meter'),
            ('OTHER', 'Other'),
        ],
        default='UNIT'
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pesticide_type = models.CharField(max_length=100, choices=PESTICIDE_TYPES)
    application_instructions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pesticide: {self.name} - {self.pesticide_type}"

class PesticideUsage(models.Model):
    pesticide = models.ForeignKey(Pesticide, on_delete=models.CASCADE, related_name='usage_records')
    field = models.ForeignKey(PlantingField, on_delete=models.SET_NULL, null=True, blank=True) 
    quantity_used = models.FloatField()  
    date_of_application = models.DateField(auto_now_add=True)  
    method_of_application = models.CharField(max_length=255, blank=True, null=True) 
    notes = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f"{self.pesticide.name} usage on {self.date_of_application}"
    
class FeedReport(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='reports')
    field = models.ForeignKey(GrazingField, on_delete=models.SET_NULL, null=True)
    quantity_used = models.FloatField()
    date_used = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.feed.name} - {self.quantity_used} {self.feed.unit_of_measure} used on {self.date_used}"