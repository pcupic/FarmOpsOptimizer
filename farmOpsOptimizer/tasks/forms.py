from django import forms
from .models import Task
from crops.models import Crop
from livestock.models import Livestock
from django.forms import DateTimeInput
from resources.models import Equipment

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'task_type',
            'start_date',
            'due_date',
            'completion_date',
            'status',
            'priority',
            'related_equipment',
            'related_crop',
            'related_livestock',
            'notes',
            'description',
        ]
        widgets = {
            'start_date': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'due_date': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'completion_date': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Provide task details...'}),
        required=False
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add additional notes...'}),
        required=False
    )

    related_equipment = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    related_crop = forms.ModelChoiceField(queryset=Crop.objects.all(), required=False)
    related_livestock = forms.ModelChoiceField(queryset=Livestock.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border border-gray-300 p-3 rounded-md'

        datetime_fields = ['start_date', 'due_date', 'completion_date']
        for field in datetime_fields:
            if self.instance and getattr(self.instance, field):
                self.fields[field].initial = getattr(self.instance, field).strftime('%Y-%m-%dT%H:%M')
