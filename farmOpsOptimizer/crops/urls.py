from django.urls import path
from . import views

app_name = 'crops'

urlpatterns = [
    path('', views.crops, name='crops'),
    path('fields/', views.fields, name='fields'),  
    path('add_crop/', views.add_crop, name='add_crop'),  
    path('add_field/', views.add_field, name='add_field'), 
    path('fields/edit/<int:field_id>/', views.edit_field, name='edit_field'), 
    path('delete_field/<int:field_id>/', views.delete_field, name='delete_field'),
    path('crops/edit/<int:crop_id>/', views.edit_crop, name='edit_crop'), 
    path('delete/<int:crop_id>/', views.delete_crop, name='delete_crop'),
    path('add-grazing-field/', views.add_grazing_field, name='add_grazing_field'),
    path('grazing-fields/', views.grazing_field_list, name='grazing_field_list'),
    path('grazing-fields/<int:pk>/edit/', views.edit_grazing_field, name='edit_grazing_field'),
    path('grazing-fields/<int:pk>/delete/', views.delete_grazing_field, name='delete_grazing_field'),   
    path('planting-report/add/<int:pk>/', views.add_planting_report, name='add_planting_report'),
    path('planting-field/<int:pk>/', views.planting_field_detail, name='planting_field_detail'),
    path('planting-report/<int:pk>/', views.planting_report_detail, name='planting_report_detail'),
    path('planting-field/<int:pk>/archive/', views.archive_all_reports, name='archive_all_reports'),
    path('fields/<int:field_id>/add-summary/', views.add_harvest_summary, name='add_harvest_summary'),
    path('grazing-field/<int:id>/', views.grazing_field_detail, name='grazing_field_detail'),
    path('crops/<int:pk>/', views.crop_detail, name='crop_detail'),
]