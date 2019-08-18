from django import forms
from .validators import validate_domainonly_username, validate_domainonly_email, validate_user_not_active, \
    validate_forbidden_characters, validate_has_digit


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50,
                               validators=[validate_user_not_active],
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Enter password'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        return password


class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50,
                               validators=[validate_domainonly_username],
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    password = forms.CharField(label='Password', max_length=50, validators=[validate_forbidden_characters],
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password',
                                                                 'placeholder': 'Enter password'}))
    first_name = forms.CharField(label='First Name', max_length=100,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(label='Last Name', max_length=100,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Enter last name'}))
    email = forms.EmailField(label='Email',
                             validators=[validate_domainonly_email],
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    phone = forms.CharField(label='Phone', max_length=30,
                            validators=[validate_has_digit],
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        return password

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        return phone
