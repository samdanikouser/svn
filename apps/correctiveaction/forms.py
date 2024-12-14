from apps.location.models import ControlPoint
from .models import CorrectiveAction
from django.forms import ModelForm
from django import forms


# define the class of a form
class ActionForm(ModelForm):
    control_point = forms.ModelChoiceField(
        queryset=ControlPoint.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),  # Disabled in the UI
        required=False
    )
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'name': "name"}),
                           error_messages={'required': "Please Enter action Name"})
    status = forms.ChoiceField(
            choices=[(True, 'Active'), (False, 'Inactive')],
            required=True,
            widget=forms.Select(attrs={'class': "form-control", 'name': 'status'})
        )
    class Meta:
        # write the name of models for which the form is made
        model = CorrectiveAction

        # Custom fields
        fields = ['control_point','name', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the control_point read-only by disabling its input in the form logic
        if self.instance and self.instance.pk:
            self.fields['control_point'].widget.attrs['readonly'] = True

    def clean(self):
        # data from the form is fetched using super function
        super(ActionForm, self).clean()

        # extract the username and text field from the data
        name = self.cleaned_data.get('name')
        status = self.cleaned_data.get('status')
        if len(name) < 5:
            self._errors['name'] = self.error_class([
                'Minimum 5 characters required'])
        # return any errors if found
        return self.cleaned_data