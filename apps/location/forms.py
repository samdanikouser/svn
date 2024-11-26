from .models import Location
from django.forms import ModelForm
from django import forms


# define the class of a form
class LocationForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'name': "name"}),
                           error_messages={'required': "Please Enter Location Name"})
    status = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class': "form-control", 'status': "status"}))

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