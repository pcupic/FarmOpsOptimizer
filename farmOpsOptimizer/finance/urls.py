from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('finances/summary/', views.planting_field_overview, name='summary'),
    path('livestock-costs/', views.livestock_costs, name='livestock_costs'),
    path('resource-assets/', views.resource_assets, name='resource_assets'),
    path('balance/', views.financial_balance, name='financial_balance'),
    path('balance/chart/', views.balance_chart_data, name='balance_chart_data'),
]
