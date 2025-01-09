from django import forms

from apps.haccp.models import CoolingData


class AddStorageDataAdminForm(forms.Form):
    name = forms.TextInput(attrs={
        'class': 'form-control text-center fw-bold',
        'style': 'max-width: auto;',
        'placeholder': 'Enter Name',
        'type': 'text'
    })
    used_for = forms.TextInput(attrs={
        'class': 'form-control text-center fw-bold',
        'style': 'max-width: auto;',
        'placeholder': 'Used For',
        'type': 'text'
    })
    num_of_used_for = forms.NumberInput(attrs={
        'class': 'form-control text-center fw-bold',
        'style': 'max-width: auto;',
        'placeholder': 'How many items'
    })
    assign_task_to = forms.TextInput(attrs={
        'class': 'form-control text-center fw-bold',
        'style': 'max-width: auto;',
        'placeholder': 'Assign Task To',
        'type': 'text'
    })
    repeat_every = forms.NumberInput(attrs={
        'class': 'form-control text-center fw-bold',
        'style': 'max-width: auto;',
        'placeholder': 'Repeat Every'
    })
    repeat_frequency = forms.TextInput(attrs={
        'class': 'form-control text-center fw-bold',
        'style': 'max-width: auto;',
        'placeholder': 'Repeat Frequency',
        'type': 'text'
    })
    time_on = forms.TimeField(widget=forms.TimeInput(attrs={
        'class': "form-control text-center fw-bold",
        'style': 'max-width: auto;',
        'placeholder': 'Please enter the shift from time',
        'type': 'time',
        'onfocus': "(this.type = 'time')"
    }))
    min_temp =  forms.NumberInput(attrs={
        'class': 'form-control text-center fw-bold',
        'style': 'max-width: auto;',
        'placeholder': 'Min Temp',
        'type': 'number',
        'step': '0.1'
    }),
    max_temp =  forms.NumberInput(attrs={
        'class': 'form-control text-center fw-bold',
        'style': 'max-width: auto;',
        'placeholder': 'Max Temp',
        'type': 'number',
        'step': '0.1'
    }),
    select_verifier = forms.TextInput(attrs={
        'class': 'form-control text-center fw-bold',
        'style': 'max-width: auto;',
        'placeholder': 'Select Verifier',
        'type': 'text'
    }),
    corrective_action = forms.CheckboxSelectMultiple(attrs={
        'class': 'form-control',
        'style': 'max-width: auto;'
    }),


class CoolingDataForm(forms.ModelForm):
    class Meta:
        model = CoolingData
        fields = [
            'storage_location', 
            'sub_storage_location', 
            'food_item', 
            'internal_temp_at_0_hrs', 
            'internal_temp_at_1_hrs', 
            'internal_temp_at_2_hrs', 
            'internal_temp_at_3_hrs', 
            'internal_temp_at_4_hrs', 
            'internal_temp_at_5_hrs', 
            'internal_temp_at_6_hrs', 
            'cooling_methods', 
            'corrective_actions', 
            'text_message'
        ]
    
    # Setting Storage Location and Sub Storage Location as read-only
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['storage_location'].widget.attrs['readonly'] = True
        self.fields['sub_storage_location'].widget.attrs['readonly'] = True

    # Setting choices for Cooling Methods
    COOLING_METHODS_CHOICES = [
        ('blast_chiller', 'Blast Chiller'),
        ('ice_water_bath', 'Ice Water Bath'),
    ]

    cooling_methods = forms.ChoiceField(
        choices=COOLING_METHODS_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False  # Optional field
    )

