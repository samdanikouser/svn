from django import forms


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


