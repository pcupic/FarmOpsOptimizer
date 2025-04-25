from django.urls import path
from . import views

app_name = 'livestock'

urlpatterns = [
    path('', views.livestock_list, name='livestock_list'),
    path('livestock/add/', views.add_livestock, name='add_livestock'),
    path('health/add/', views.add_health_record, name='add_health_record'),
    path('vaccination/add/', views.add_vaccination_record, name='add_vaccination_record'),
    path('species/', views.species_list, name='species_list'),  
    path('species/add/', views.species_add, name='species_add'), 
    path('species/<int:pk>/', views.species_detail, name='species_detail'),
    path('livestock/<int:id>/', views.livestock_detail, name='livestock_detail'), 
    path('herds/', views.herd_list, name='herd_list'),
    path('herds/add/', views.add_herd, name='add_herd'),
    path('herds/<int:pk>/', views.herd_detail, name='herd_detail'),
    path('herds/<int:herd_id>/add-livestock/', views.add_livestock_to_herd, name='add_livestock_to_herd'),
    path('<int:pk>/add-health-record/', views.add_health_record, name='add_health_record'),
    path('<int:pk>/add-vaccination/', views.add_vaccination_record, name='add_vaccination_record'),
    path('pending-species/', views.pending_species_list, name='pending_species_list'),
    path('species/<int:pk>/approve/', views.approve_species, name='approve_species'),
    path('species/<int:pk>/delete/', views.delete_species, name='delete_species'),
    path('health_record/<int:id>/', views.health_record_detail, name='health_record_detail'),
    path('vaccination/<int:id>/', views.vaccination_detail, name='vaccination_detail'),
    path('livestock/<int:pk>/edit/', views.edit_livestock, name='edit_livestock'),
    path('livestock/<int:pk>/delete/', views.delete_livestock, name='delete_livestock'),
    path('edit/<int:pk>/', views.edit_livestock, name='edit_livestock'),
]
