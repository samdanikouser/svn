# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from apps.authentication.models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class UsernamePasswordResetForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Username",
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
    )

    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter a new password'}),
        help_text="Your password must contain at least 8 characters."
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract the user from kwargs
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username  # Set initial username from user object

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username does not exist.")
        return username

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if len(password) < 10:  # Ensure password length is at least 10 characters
            raise forms.ValidationError("The new password must be at least 10 characters long.")
        return password

class UserUpdateForm(ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'readonly': 'readonly', 'class': 'form-control'}),  # Use readonly
        required=False
    )

    role = forms.ChoiceField(
        choices=[
            ('line_staff', 'Line Staff'),
            ('supervisors', 'Supervisors'),
            ('managers', 'Managers'),
            ('admin', 'Admin'),
            ('e_learning', 'e-Learning'),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        )
    )
    status = forms.BooleanField(required=False,
                                widget=forms.CheckboxInput(attrs={'class': "form-control", 'status': "status"}))

    class Meta:
        model = UserProfile
        fields = ('user', 'role', 'status')