from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import models

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = models.User
        fields = ["email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = ' '    

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    password = forms.PasswordInput()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = ' '   