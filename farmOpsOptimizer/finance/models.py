from django.db import models

class FinancialRecord(models.Model):
    RECORD_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]
    
    record_type = models.CharField(max_length=10, choices=RECORD_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True) 

    def __str__(self):
        return f"{self.record_type}: {self.amount} on {self.date}"
