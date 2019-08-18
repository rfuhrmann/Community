from django import forms
from django.core.exceptions import ValidationError
from .validators import validate_domainonly_username, validate_domainonly_email, validate_user_not_active
from django.db.models import Q
from users.models import Friendship
from django.contrib.auth import get_user_model

User = get_user_model()


class StatusForm(forms.Form):
    title = forms.CharField(label='Title', max_length=254,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}))
    message = forms.CharField(label='Message', max_length=254,
                              widget=forms.Textarea(
                                  attrs={'class': 'form-control', 'placeholder': 'Enter message', 'rows': 2}))

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_message(self):
        message = self.cleaned_data['message']
        return message


class StatusCommentForm(forms.Form):
    comment_message = forms.CharField(label='Message', max_length=254,
                                      widget=forms.Textarea(
                                          attrs={'class': 'form-control', 'placeholder': 'Enter message', 'rows': 2}))

    def clean_comment_message(self):
        comment_message = self.cleaned_data['comment_message']
        return comment_message


class FriendForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50,
                               validators=[validate_domainonly_username],
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    # hidden field for friendship request
    # is filled with initial current username in view
    current_username = forms.CharField(label='', max_length=50,
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control', 'placeholder': 'Enter current_username',
                                                  'hidden': True}))

    # check if friendship or request exists
    # request is possible, if friendship is rejected or declined
    def clean(self):
        cleaned_data = super(FriendForm, self).clean()
        u1 = cleaned_data.get("username")
        u2 = cleaned_data.get("current_username")
        if u1 and u2:
            user1 = User.objects.get(username=u1)
            user2 = User.objects.get(username=u2)
            qs1 = Friendship.objects.filter(Q(sender=user1) & Q(recipient=user2) & (
                    Q(status="request") | Q(status="accepted")))
            qs2 = Friendship.objects.filter(Q(sender=user2) & Q(recipient=user1) & (
                    Q(status="request") | Q(status="accepted")))
            print(qs1.count(), qs2.count())
            if qs1.count() > 0 or qs2.count() > 0:
                raise forms.ValidationError("Friendship request already exists")
            elif user1 == user2:
                print(" username == current_username")
                raise forms.ValidationError("Please choose a second person for a friendship")


class ContactForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(label='Last Name', max_length=100,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Enter last name'}))
    email = forms.EmailField(label='Email', disabled=True,
                             validators=[validate_domainonly_email],
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    phone = forms.CharField(label='Phone', max_length=30,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone'}))

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


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User

    def clean_password(self):
        password = self.cleaned_data['password']
        return password


class AddressForm(forms.Form):
    country = forms.CharField(max_length=254,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter country'}))
    postal_code = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter postal code'}))
    town = forms.CharField(max_length=254,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter town'}))
    street = forms.CharField(max_length=254,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter street'}))
    street_number = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter street number'}))

    def clean_country(self):
        country = self.cleaned_data['country']
        return country

    def clean_postal_code(self):
        postal_code = self.cleaned_data['postal_code']
        return postal_code

    def clean_town(self):
        town = self.cleaned_data['town']
        return town

    def clean_street(self):
        street = self.cleaned_data['street']
        return street

    def clean_street_number(self):
        street_number = self.cleaned_data['street_number']
        return street_number


class PrivacyForm(forms.Form):
    contact = forms.BooleanField(label='Show contact', required=False)
    address = forms.BooleanField(label='Show address', required=False)
    status_comments = forms.BooleanField(label='Show status comments', required=False)
    friends = forms.BooleanField(label='Show friends', required=False)
    discussions = forms.BooleanField(label='Show discussions', required=False)
    events = forms.BooleanField(label='Show events', required=False)
    groups = forms.BooleanField(label='Show groups', required=False, disabled=True)

    def clean_contact(self):
        contact = self.cleaned_data['contact']
        return contact

    def clean_address(self):
        address = self.cleaned_data['address']
        return address

    def clean_status_comments(self):
        status_comments = self.cleaned_data['status_comments']
        return status_comments

    def clean_friends(self):
        friends = self.cleaned_data['friends']
        return friends

    def clean_discussions(self):
        discussions = self.cleaned_data['discussions']
        return discussions

    def clean_events(self):
        events = self.cleaned_data['events']
        return events

    def clean_groups(self):
        groups = self.cleaned_data['groups']
        return groups


class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50, disabled=True, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    password = forms.CharField(label='Password', max_length=50, disabled=True, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password',
                                                             'placeholder': 'Enter password'}))
    first_name = forms.CharField(label='First Name', max_length=100,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(label='Last Name', max_length=100,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Enter last name'}))
    email = forms.EmailField(label='Email', disabled=True, required=False,
                             validators=[validate_domainonly_email],
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    phone = forms.CharField(label='Phone', max_length=30,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone'}))

    def clean_password(self):
        password = self.cleaned_data['password']
        return password

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return last_name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        return phone


class ImageForm(forms.Form):
    img = forms.ImageField()
    def clean_img(self):
        img = self.cleaned_data['img']
        return img
