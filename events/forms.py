# from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, \
#     YearPickerInput
from django import forms
from events.models import Event, EventInvitation
from .validators import validate_domainonly_username
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class EventForm(forms.Form):
    name = forms.CharField(label="Name", max_length=254,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}))
    description = forms.CharField(label="Description", widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 2}))
    category = forms.ChoiceField(label="Category", choices=Event.CATEGORIES,
                                 widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter category'}))
    # start_datetime = forms.DateTimeField(label="Start datetime",
    #                                      widget=DateTimePickerInput(attrs={'placeholder': 'Choose start datetime'}))
    # end_datetime = forms.DateTimeField(label="End datetime",
    #                                    widget=DateTimePickerInput(attrs={'placeholder': 'Choose end datetime'}))
    start_datetime = forms.DateTimeField(label="Start time", widget=forms.DateTimeInput(
        attrs={'class': 'form-control', 'placeholder': 'yyyy-mm-dd hh:mm'}))
    end_datetime = forms.DateTimeField(label="End time", widget=forms.DateTimeInput(
        attrs={'class': 'form-control', 'placeholder': 'yyyy-mm-dd hh:mm'}))
    place_name = forms.CharField(max_length=254,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Place'}))
    place_description = forms.CharField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter place description'}))

    # address = forms.BooleanField(label='Add address', required=False)
    # country = forms.CharField(label='Country', max_length=254,
    #                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter country'}))
    # postal_code = forms.IntegerField(
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter postal code'}))
    # town = forms.CharField(max_length=254,
    #                        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter town'}))
    # street = forms.CharField(max_length=254,
    #                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter street'}))
    # street_number = forms.IntegerField(
    #     widget=forms.TextInput(
    #         attrs={'class': 'form-control', 'placeholder': 'Enter street number'}))

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(EventForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['place_name'].required = False
        self.fields['place_description'].required = False
        # self.fields['country'].required = False
        # self.fields['postal_code'].required = False
        # self.fields['town'].required = False
        # self.fields['street'].required = False
        # self.fields['street_number'].required = False

    def clean_name(self):
        name = self.cleaned_data['name']
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        return description

    def clean_category(self):
        category = self.cleaned_data['category']
        return category

    def clean_start_datetime(self):
        start_datetime = self.cleaned_data['start_datetime']
        return start_datetime

    def clean_end_datetime(self):
        end_datetime = self.cleaned_data['end_datetime']
        return end_datetime

    # def clean_place(self):
    #     place = self.cleaned_data['place']
    #     return place

    def clean_place_name(self):
        place_name = self.cleaned_data['place_name']
        return place_name

    def clean_place_description(self):
        place_description = self.cleaned_data['place_description']
        return place_description

    # def clean_address(self):
    #     address = self.cleaned_data['address']
    #     return address
    #
    # def clean_country(self):
    #     country = self.cleaned_data['country']
    #     return country
    #
    # def clean_postal_code(self):
    #     postal_code = self.cleaned_data['postal_code']
    #     return postal_code
    #
    # def clean_town(self):
    #     town = self.cleaned_data['town']
    #     return town
    #
    # def clean_street(self):
    #     street = self.cleaned_data['street']
    #     return street
    #
    # def clean_street_number(self):
    #     street_number = self.cleaned_data['street_number']
    #     return street_number


class ParticipantForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50,
                               validators=[validate_domainonly_username],
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    # hidden field for friendship request
    # is filled with initial current username in view
    current_username = forms.CharField(label='', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'hidden': True}))
    event_id = forms.IntegerField(label='', widget=forms.HiddenInput())

    # check if user == owner or participant
    def clean(self):
        cleaned_data = super(ParticipantForm, self).clean()
        u1 = cleaned_data.get("username")
        u2 = cleaned_data.get("current_username")
        # if name wrong => return and run into validator error
        if not (u1 and u2):
            return
        # if user == event.owner
        if u1 == u2:
            raise forms.ValidationError("You are already a part of the event")
        user = User.objects.get(username=u1)
        curr_user = User.objects.get(username=u2)
        # if user is not a friend of curr_user
        if user not in curr_user.friends.all():
            raise forms.ValidationError("You can only invite friends")
        # if user is participant
        e = Event.objects.get(pk=cleaned_data.get("event_id"))
        if e:
            p_exists = False
            if e.participants:
                if user in e.participants.all():
                    p_exists = True
            if p_exists:
                raise forms.ValidationError("User is already a participant")

            i_exists = False
            if e.invitations:
                i_exists = EventInvitation.objects.filter(Q(recipient=user) & Q(status="request")).exists()
            if i_exists:
                raise forms.ValidationError("User is already invited")

    def clean_username(self):
        username = self.cleaned_data['username']
        return username
