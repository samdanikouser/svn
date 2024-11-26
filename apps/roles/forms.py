from .models import Roles
from django.forms import ModelForm
from django import forms


# define the class of a form
class RoleForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'name': "name"}),
                           error_messages={'required': "Please Enter Role Name"})
    class Meta:
        # write the name of models for which the form is made
        model = Roles

        # Custom fields
        fields = ['name']

    def clean(self):
        # data from the form is fetched using super function
        super(RoleForm, self).clean()

        # extract the username and text field from the data
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            self._errors['name'] = self.error_class([
                'Minimum 3 characters required'])
        # return any errors if found
        return self.cleaned_data