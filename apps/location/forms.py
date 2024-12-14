from .models import ControlPoint, Location
from django.forms import ModelForm
from django import forms


# define the class of a form
class LocationForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'name': "name"}),
                           error_messages={'required': "Please Enter Location Name"})
    status = forms.ChoiceField(
            choices=[(True, 'Active'), (False, 'Inactive')],
            required=True,
            widget=forms.Select(attrs={'class': "form-control", 'name': 'status'})
        )

    class Meta:
        # write the name of models for which the form is made
        model = Location

        # Custom fields
        fields = ['name', 'status']

    def clean(self):
        # data from the form is fetched using super function
        super(LocationForm, self).clean()

        # extract the username and text field from the data
        name = self.cleaned_data.get('name')
        status = self.cleaned_data.get('status')
        if len(name) < 5:
            self._errors['name'] = self.error_class([
                'Minimum 5 characters required'])
        # return any errors if found
        return self.cleaned_data
    

class ControlPointForm(forms.ModelForm):
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        widget=forms.Select(attrs={'readonly': 'readonly', 'class': 'form-control'}),  # Use readonly
        required=False
    )
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'name': "name"}),
                           error_messages={'required': "Please Enter Control point Name"})
    daily_activity = forms.ChoiceField(
            choices=[(True, 'Active'), (False, 'Inactive')],
            required=True,
            widget=forms.Select(attrs={'class': "form-control", 'name': 'status'})
        )
    status = forms.ChoiceField(
            choices=[(True, 'Active'), (False, 'Inactive')],
            required=True,
            widget=forms.Select(attrs={'class': "form-control", 'name': 'status'})
        )

    class Meta:
        model = ControlPoint
        fields = ['location', 'name', 'daily_activity', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the location field as read-only
        if 'location' in self.fields:
            self.fields['location'].widget.attrs['readonly'] = True
            # Optionally disable the location field to prevent user editing
            self.fields['location'].disabled = True
