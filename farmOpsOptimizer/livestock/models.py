from django.db import models
from crops.models import GrazingField
from django.contrib.auth.models import User

class Species(models.Model):
    name = models.CharField(max_length=100)  
    description = models.TextField()  

    scientific_name = models.CharField(max_length=100, blank=True, null=True) 
    family = models.CharField(max_length=100, blank=True, null=True) 
    genus = models.CharField(max_length=100, blank=True, null=True)  
    kingdom = models.CharField(max_length=100, blank=True, null=True)  

    CONSERVATION_STATUS_CHOICES = [
        ('LC', 'Least Concern'),
        ('NT', 'Near Threatened'),
        ('VU', 'Vulnerable'),
        ('EN', 'Endangered'),
        ('CR', 'Critically Endangered'),
        ('EX', 'Extinct'),
        ('EW', 'Extinct in the Wild'),
    ]
    conservation_status = models.CharField(max_length=2, choices=CONSERVATION_STATUS_CHOICES, default='LC')

    AVERAGE_WEIGHT_CHOICES = [
        ('<10', 'Less than 10kg'),
        ('10-50', '10-50kg'),
        ('50-100', '50-100kg'),
        ('100-500', '100-500kg'),
        ('>500', 'More than 500kg'),
    ]
    average_weight = models.CharField(max_length=10, choices=AVERAGE_WEIGHT_CHOICES, blank=True, null=True) 

    AVERAGE_HEIGHT_CHOICES = [
        ('<0.5', 'Less than 0.5m'),
        ('0.5-1', '0.5-1m'),
        ('1-3', '1-3m'),
        ('3-5', '3-5m'),
        ('>5', 'More than 5m'),
    ]
    average_height = models.CharField(max_length=10, choices=AVERAGE_HEIGHT_CHOICES, blank=True, null=True) 
    LIFESPAN_CHOICES = [
            (1, 'Less than 1 year'),
            (2, '1-5 years'),
            (3, '6-10 years'),
            (4, '11-20 years'),
            (5, '21-50 years'),
            (6, 'More than 50 years'),
        ]
    lifespan = models.IntegerField(choices=LIFESPAN_CHOICES, null=True, blank=True)

    habitat = models.TextField(blank=True, null=True)  
    RANGE_CHOICES = [
        ('AFRICA', 'Africa'),
        ('ASIA', 'Asia'),
        ('EUROPE', 'Europe'),
        ('NORTH_AMERICA', 'North America'),
        ('SOUTH_AMERICA', 'South America'),
        ('OCEANIA', 'Oceania'),
        ('ANTARCTICA', 'Antarctica'),
        ('GLOBAL', 'Global'),
    ]
    range = models.CharField(max_length=15, choices=RANGE_CHOICES, blank=True, null=True)  

    DIET_CHOICES = [
        ('HERBIVORE', 'Herbivore'),
        ('CARNIVORE', 'Carnivore'),
        ('OMNIVORE', 'Omnivore'),
        ('INSECTIVORE', 'Insectivore'),
        ('FRUGIVORE', 'Frugivore'),
        ('NECROPHAGY', 'Necrophagy'),
    ]
    diet = models.CharField(max_length=20, choices=DIET_CHOICES, blank=True, null=True) 

    BEHAVIOR_CHOICES = [
        ('SOCIAL', 'Social'),
        ('SOLITARY', 'Solitary'),
        ('MIGRATORY', 'Migratory'),
        ('NOCTURNAL', 'Nocturnal'),
        ('DIURNAL', 'Diurnal'),
    ]
    behavior = models.CharField(max_length=20, choices=BEHAVIOR_CHOICES, blank=True, null=True)  

    REPRODUCTION_CHOICES = [
        ('OVIPAROUS', 'Oviparous'),
        ('VIVIPAROUS', 'Viviparous'),
        ('OVOVIVIPAROUS', 'Ovoviviparous'),
    ]
    reproduction = models.CharField(max_length=25, choices=REPRODUCTION_CHOICES, blank=True, null=True)  
    MATING_SEASON_CHOICES = [
            ('SPRING', 'Spring'),
            ('SUMMER', 'Summer'),
            ('AUTUMN', 'Autumn'),
            ('WINTER', 'Winter'),
            ('YEAR_ROUND', 'Year-Round'),
            ('UNKNOWN', 'Unknown'), 
        ]

    mating_season = models.CharField(max_length=20, choices=MATING_SEASON_CHOICES, blank=True, null=True)

    ENDANGERED_STATUS_CHOICES = [
        ('CRITICALLY_ENDANGERED', 'Critically Endangered'),
        ('ENDANGERED', 'Endangered'),
        ('VULNERABLE', 'Vulnerable'),
        ('NEAR_THREATENED', 'Near Threatened'),
        ('LEAST_CONCERN', 'Least Concern'),
        ('DATA_DEFICIENT', 'Data Deficient'),
        ('NOT_EVALUATED', 'Not Evaluated'),
        ('UNKNOWN', 'Unknown'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='approved')
    endangered_status = models.CharField(max_length=25, choices=ENDANGERED_STATUS_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name

class Herd(models.Model):
    name = models.CharField(max_length=100)
    field = models.ForeignKey(GrazingField, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='herds')  
    species = models.ForeignKey(Species, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def livestock_count(self):
      return self.livestock.count()

class Livestock(models.Model):
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ]
    
    species = models.ForeignKey(Species, on_delete=models.CASCADE)  
    name = models.CharField(max_length=100)  
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='MALE')
    birth_date = models.DateTimeField(null=True, blank=True) 
    weight = models.FloatField(null=True, blank=True)  
    breed = models.CharField(max_length=100, blank=True, null=True)  
    grazing_field = models.ForeignKey(GrazingField, on_delete=models.SET_NULL, null=True, blank=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='livestocks', null=True)  
    herd = models.ForeignKey(Herd, on_delete=models.SET_NULL, null=True, blank=True, related_name='livestock')

    def __str__(self):
        return f"{self.name} ({self.species.name})"

class HealthRecord(models.Model):
    HEALTH_STATUS_CHOICES = [
        ('HEALTHY', 'Healthy'),
        ('ILL', 'Ill'),
        ('INJURED', 'Injured'),
        ('VACCINATED', 'Vaccinated'),
        ('RECOVERING', 'Recovering'),
        ('QUARANTINED', 'Quarantined'),
        ('UNDER_OBSERVATION', 'Under Observation'),
        ('DECEASED', 'Deceased'),
    ]
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MODERATE', 'Moderate'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    livestock = models.ForeignKey(Livestock, on_delete=models.CASCADE, related_name='health_records')
    health_status = models.CharField(max_length=20, choices=HEALTH_STATUS_CHOICES, blank=True, null=True)
    severity_level = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    cost_of_treatment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_recorded = models.DateField(auto_now_add=True)
    next_checkup_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Health record for {self.livestock.name} on {self.date_recorded}"


class VaccinationRecord(models.Model):
    VACCINATION_CHOICES = [
        ('RABIES', 'Rabies'),
        ('BOVINE_TB', 'Bovine Tuberculosis'),
        ('BRUCELLOSIS', 'Brucellosis'),
        ('IBR', 'Infectious Bovine Rhinotracheitis'),
        ('BVD', 'Bovine Viral Diarrhea'),
        ('LEPTOSPIROSIS', 'Leptospirosis'),
        ('BLACKLEG', 'Blackleg'),
        ('FOOT_AND_MOUTH', 'Foot and Mouth Disease'),
        ('ANTHRAX', 'Anthrax'),
        ('BLUETONGUE', 'Bluetongue'),
        ('SHEEP_POX', 'Sheep Pox'),
        ('OVINE_TACHENG', 'Ovine Tacheng'),
        ('SHEEP_ERYSIPELOTHRIX', 'Erysipelothrix (Sheep)'),
        ('MASTITIS', 'Mastitis Vaccine'),
        ('CSF', 'Classical Swine Fever'),
        ('ASF', 'African Swine Fever'),
        ('SWINE_INFLUENZA', 'Swine Influenza'),
        ('TETANUS', 'Tetanus'),
        ('HOG_CHOLERA', 'Hog Cholera'),
        ('CHICKEN_POX', 'Chickenpox'),
        ('AVIAN_FLU', 'Avian Influenza'),
        ('NEWCASTLE_DISEASE', 'Newcastle Disease'),
        ('FOWL_POX', 'Fowl Pox'),
        ('SALMONELLOSIS', 'Salmonellosis'),
        ('CAMPYLOBACTERIOSIS', 'Campylobacteriosis'),
        ('PARVOVIRUS', 'Parvovirus'),
        ('LEUKEMIA', 'Leukemia'),
        ('TUBERCULOSIS', 'Tuberculosis (Bovine)'),
        ('EPM', 'Equine Protozoal Myeloencephalitis'),
        ('ROTAVIRUS', 'Rotavirus'),
        ('CALF_DIARRHEA', 'Calf Diarrhea Vaccine'),
        ('HEARTWORM', 'Heartworm Vaccine'),
        ('FLEA_TICK', 'Flea and Tick Prevention'),
        ('INFLUENZA_A', 'Influenza A Vaccine'),
        ('RHINO', 'Rhinovirus'),
        ('OTHER', 'Other') 
    ]

    livestock = models.ForeignKey(Livestock, on_delete=models.CASCADE, related_name='vaccination_records')
    vaccination_name = models.CharField(max_length=100, choices=VACCINATION_CHOICES) 
    vaccination_date = models.DateField()  
    next_due_date = models.DateField(null=True, blank=True) 
    custom_vaccination_name = models.CharField(max_length=100, blank=True, null=True)  
    cost_of_vaccine = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Vaccination record for {self.livestock.name} on {self.vaccination_date}"

    def save(self, *args, **kwargs):
        if self.vaccination_name == 'OTHER' and not self.custom_vaccination_name:
            raise ValueError("Please specify a custom vaccination name if 'Other' is selected.")
        super().save(*args, **kwargs)



