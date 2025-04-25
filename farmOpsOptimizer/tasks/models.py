from django.db import models
from django.contrib.auth.models import User
from datetime import date
from crops.models import Crop
from livestock.models import Livestock
from resources.models import Equipment

class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    TASK_TYPE_CHOICES = [
        ('PLANTING', 'Planting'),
        ('HARVESTING', 'Harvesting'),
        ('IRRIGATION', 'Irrigation'),
        ('MAINTENANCE', 'Maintenance'),
        ('FERTILIZING', 'Fertilizing'),
        ('PEST_CONTROL', 'Pest Control'),
        ('FEEDING', 'Feeding'),
        ('INSPECTION', 'Inspection'),
        ('OTHER', 'Other'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    task_type = models.CharField(max_length=30, choices=TASK_TYPE_CHOICES, default='OTHER')
    start_date = models.DateTimeField(default=date.today)
    due_date = models.DateTimeField()
    completion_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    notes = models.TextField(blank=True, null=True)
    related_equipment = models.ManyToManyField(Equipment, blank=True)
    related_crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, blank=True)
    related_livestock = models.ForeignKey(Livestock, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} ({self.status})"
