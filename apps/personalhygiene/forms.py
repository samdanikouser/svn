from django import forms
from .models import PersonalHygiene, UploadedPhoto

class PersonalHygieneForm(forms.ModelForm):
    photos = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False
    )

    class Meta:
        model = PersonalHygiene
        fields = [
            'employee',
            'inspected_date',
            'inspected_by',
            'parameters_checked',
            'status',
            'photos',
        ]
        widgets = {
            'inspected_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        """
        Override save method to handle multiple photo uploads.
        """
        instance = super().save(commit=False)

        # Save the instance first if commit=True
        if commit:
            instance.save()

        # Handle photos field
        if self.cleaned_data.get('photos'):
            for photo_file in self.cleaned_data['photos']:
                photo_instance = UploadedPhoto(photo=photo_file)
                photo_instance.save()
                instance.photos.add(photo_instance)

        return instance
