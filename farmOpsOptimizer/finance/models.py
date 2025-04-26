from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class DailyBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    income = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    expenses = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['date']
        
    def __str__(self):
        return f"{self.user.username} - {self.date}: Balance {self.balance}"

