from django import forms
from .models import Crop, GrazingField, PlantingField, PlantingReport, HarvestSummary
from django.contrib.auth.models import User

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = [
            'name', 'type', 'sowing_time', 'harvesting_time_start', 'harvesting_time_end',
            'optimal_conditions', 'botanical_name', 'row_spacing', 'planting_depth',
            'average_height', 'plant_spacing', 'days_to_emerge', 'days_to_flower',
            'days_to_maturity', 'estimated_revenue_per_harvest_unit',
            'estimated_yield_per_ha', 'manufacturer', 'variety_type'
        ]
        widgets = {
            'seed_cost_per_ton': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'seed_quantity_in_tons': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'sowing_time': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'harvesting_time_start': forms.DateTimeInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'type': 'datetime-local'
            }),
            'harvesting_time_end': forms.DateTimeInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'type': 'datetime-local'
            }),
            'optimal_conditions': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'rows': 4
            }),
            'botanical_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'row_spacing': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'planting_depth': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'average_height': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'plant_spacing': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'days_to_emerge': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'days_to_flower': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'days_to_maturity': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'estimated_revenue_per_harvest_unit': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'step': '0.01'
            }),
            'estimated_yield_per_ha': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'step': '0.01'
            }),
            'manufacturer': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'variety_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
        }

class PlantingFieldForm(forms.ModelForm):
    class Meta:
        model = PlantingField
        fields = [
            'name', 'area', 'soil_type', 'crop', 'planting_date', 'estimated_value', 'light_profile'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'area': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'soil_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'crop': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'planting_date': forms.DateTimeInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'type': 'datetime-local'
            }),
            'estimated_value': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'step': '0.01'
            }),
            'light_profile': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
        }
        
class GrazingFieldForm(forms.ModelForm):
    class Meta:
        model = GrazingField
        fields = [
            'name', 'area', 'grazing_rest_days', 'estimated_value', 'water_source'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'area': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'grazing_rest_days': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'estimated_value': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'step': '0.01'
            }),
            'water_source': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
        }

class PlantingReportForm(forms.ModelForm):
    class Meta:
        model = PlantingReport
        fields = ['plant_height', 'plant_health', 'flowering_status', 
                  'maturity_status', 'temperature', 'humidity', 'notes']
        
        widgets = {
            'plant_height': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'placeholder': 'Enter plant height in cm'
            }),
            'plant_health': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'placeholder': 'Enter plant health status'
            }),
            'flowering_status': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'maturity_status': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'temperature': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'placeholder': 'Enter temperature in °C'
            }),
            'humidity': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'placeholder': 'Enter humidity in %'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'placeholder': 'Additional notes about the planting process'
            }),
        }
        
class HarvestSummaryForm(forms.ModelForm):
    class Meta:
        model = HarvestSummary
        fields = ['season', 'yield_in_tons', 'price_per_ton', 'notes']
        
        widgets = {
            'season': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'placeholder': 'Enter season'
            }),
            'yield_in_tons': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'placeholder': 'Enter yield in tons'
            }),
            'price_per_ton': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'placeholder': 'Enter price per ton'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'placeholder': 'Enter additional notes (optional)'
            }),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        
        yield_in_tons = cleaned_data.get('yield_in_tons')
        price_per_ton = cleaned_data.get('price_per_ton')
        
        if yield_in_tons is not None and price_per_ton is not None:
            cleaned_data['total_revenue'] = yield_in_tons * price_per_ton
        
        return cleaned_data