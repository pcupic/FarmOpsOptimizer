from django import forms
from .models import Equipment, Seed, SeedUsage, MaintenanceRecord, Fertilizer, FertilizerUsage, Pesticide, PesticideUsage, Feed, FeedReport

class SeedForm(forms.ModelForm):
    class Meta:
        model = Seed
        fields = [
            'name',
            'unit_of_measure',
            'quantity',
            'price_per_unit',
            'crop',
            'sowing_instructions',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'unit_of_measure': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'step': '0.01'
            }),
            'price_per_unit': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'step': '0.01'
            }),
            'crop': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'sowing_instructions': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'rows': 3
            }),
        }

class SeedUsageForm(forms.ModelForm):
    class Meta:
        model = SeedUsage
        fields = ['seed', 'quantity_used']
        widgets = {
            'seed': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'quantity_used': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'step': '0.01'
            }),
        }

    def __init__(self, *args, **kwargs):
        crop = kwargs.pop('crop', None)  
        super().__init__(*args, **kwargs)
        if crop:
            self.fields['seed'].queryset = Seed.objects.filter(crop=crop)

    def clean_quantity_used(self):
        quantity_used = self.cleaned_data.get('quantity_used')
        if quantity_used <= 0:
            raise forms.ValidationError('Quantity used must be greater than 0.')
        
        seed = self.cleaned_data.get('seed')
        if seed and quantity_used > seed.quantity:
            raise forms.ValidationError(f"Not enough seed in stock (available: {seed.quantity}).")
        return quantity_used


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'value', 'condition','last_maintenance_date', 'purchase_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'condition': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'value': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'step': '0.01'
            }),
            'last_maintenance_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'purchase_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
        }

class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = ['description', 'cost']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'rows': 4
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'step': '0.01'
            }),
        }
        
class FertilizerForm(forms.ModelForm):
    class Meta:
        model = Fertilizer
        fields = ['name', 'quantity', 'price_per_unit', 'fertilizer_type', 'unit_of_measure', 'application_instructions']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'min': '0',
            }),
            'price_per_unit': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'min': '0',
                'step': '0.01',
            }),
            'fertilizer_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'unit_of_measure': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'application_instructions': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
            }),
        }

        
class FertilizerUsageForm(forms.ModelForm):
    class Meta:
        model = FertilizerUsage
        fields = ['fertilizer', 'amount_used', 'notes']
        widgets = {
            'fertilizer': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md',
            }),
            'amount_used': forms.NumberInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md',
                'step': '0.01',
                'min': '0'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md',
                'rows': 3,
                'placeholder': 'Optional notes...'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['fertilizer'].queryset = Fertilizer.objects.filter(user=user)


class PesticideForm(forms.ModelForm):
    class Meta:
        model = Pesticide
        fields = ['name', 'quantity', 'price_per_unit', 'pesticide_type', 'unit_of_measure', 'application_instructions']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'min': '0',
            }),
            'price_per_unit': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'min': '0',
                'step': '0.01',
            }),
            'pesticide_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'unit_of_measure': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'application_instructions': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
            }),
        }

        
class PesticideUsageForm(forms.ModelForm):
    class Meta:
        model = PesticideUsage
        fields = [
            'pesticide', 
            'quantity_used', 
            'method_of_application', 
            'notes',
        ]
        widgets = {
            'pesticide': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'quantity_used': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'step': '0.01'
            }),
            'method_of_application': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'rows': 3
            }),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)

        if user:
            self.fields['pesticide'].queryset = Pesticide.objects.filter(user=user)
            
            
class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = [
            'unit_of_measure',
            'name',
            'quantity',
            'price_per_unit',
            'food_type',
            'feeding_instructions',
        ]
        widgets = {
            'unit_of_measure': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'step': '0.01'
            }),
            'price_per_unit': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'step': '0.01'
            }),
            'feeding_instructions': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'rows': 3
            }),
            'food_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['price_per_unit'].required = True
        self.fields['quantity'].required = True

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        return quantity if quantity is not None else 0

        
class FeedReportForm(forms.ModelForm):
    class Meta:
        model = FeedReport
        fields = [
            'feed',
            'quantity_used',
            'notes',
        ]
        widgets = {
            'feed': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'quantity_used': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'step': '0.01'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'rows': 3
            }),
        }