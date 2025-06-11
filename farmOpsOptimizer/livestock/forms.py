from django import forms
from .models import Livestock, HealthRecord, VaccinationRecord, Species, Herd
from crops.models import GrazingField

    
class LivestockForm(forms.ModelForm):
    class Meta:
        model = Livestock
        fields = ['species', 'name', 'gender', 'birth_date', 'weight', 'breed', 'herd', 'grazing_field']
        widgets = {
            'species': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'type': 'date'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'breed': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'grazing_field': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'herd': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super(LivestockForm, self).__init__(*args, **kwargs)

        self.fields['species'].required = True

        if user:
            self.fields['grazing_field'].queryset = GrazingField.objects.filter(user=user)

        
        
class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = [
            'health_status',
            'severity_level',
            'description',
            'symptoms',
            'treatment',
            'cost_of_treatment',
            'next_checkup_date',
        ]
        widgets = {
            'health_status': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'severity_level': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg resize-y focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'rows': 3,
                'placeholder': 'Brief overview of the issue...'
            }),
            'symptoms': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg resize-y focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'rows': 3,
                'placeholder': 'Describe symptoms in detail...'
            }),
            'treatment': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg resize-y focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'rows': 3,
                'placeholder': 'Describe the treatment plan...'
            }),
            'cost_of_treatment': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
                'step': '0.01',
                'placeholder': '€'
            }),
            'next_checkup_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500'
            }),
        }

class VaccinationRecordForm(forms.ModelForm):
    class Meta:
        model = VaccinationRecord
        fields = [
            'vaccination_name',
            'custom_vaccination_name',
            'vaccination_date',
            'next_due_date',
            'cost_of_vaccine',
        ]
        widgets = {
            'vaccination_name': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'custom_vaccination_name': forms.TextInput(attrs={
                'placeholder': 'Specify if "Other"',
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'vaccination_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'next_due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'cost_of_vaccine': forms.NumberInput(attrs={
                'step': '0.01',
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
        }

class SpeciesForm(forms.ModelForm):
    class Meta:
        model = Species
        fields = ['name', 'scientific_name', 'family', 'genus', 'kingdom', 
                  'conservation_status', 'average_weight', 'average_height', 'lifespan', 
                  'range', 'diet', 'behavior', 'reproduction', 'mating_season', 
                  'endangered_status', 'habitat', 'description']
        widgets = {
    'name': forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
    }),
    'scientific_name': forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
    }),
    'family': forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
    }),
    'genus': forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
    }),
    'kingdom': forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
    }),
    'conservation_status': forms.Select(attrs={
        'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
    }),
    'average_weight': forms.Select(attrs={
        'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
    }),
    'average_height': forms.Select(attrs={
        'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
    }),
    'lifespan': forms.Select(attrs={
        'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
    }),
    'range': forms.Select(attrs={
        'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
    }),
    'diet': forms.Select(attrs={
        'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
    }),
    'behavior': forms.Select(attrs={
        'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
    }),
    'reproduction': forms.Select(attrs={
        'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
    }),
    'mating_season': forms.Select(attrs={
        'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
    }),
    'endangered_status': forms.Select(attrs={
        'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
    }),
    'description': forms.Textarea(attrs={
        'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
        'rows': 3
    }),
    'habitat': forms.Textarea(attrs={
        'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500',
        'rows': 2
    }),
}

class HerdForm(forms.ModelForm):
    class Meta:
        model = Herd
        fields = ['name', 'field', 'species']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'field': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
            'species': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500'
            }),
        }
        
    def __init__(self, request, *args, **kwargs, ):
        super(HerdForm, self).__init__(*args, **kwargs)
        
        self.fields['field'].required = True
        self.fields['field'].queryset = GrazingField.objects.filter(user=request.user)  
        
        self.fields['species'].required = True
