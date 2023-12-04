'''This module holds the forms for User creation.'''
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomSignUpForm(UserCreationForm):
    '''Represents a form for users to sign up--extends the user form to also include an email'''
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        '''Meta data for the form.'''
        model = User
        fields = ('username', 'email', 'password1')
        