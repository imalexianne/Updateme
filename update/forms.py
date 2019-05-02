from django import forms
from .models import Profile,Event,Ticket

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'pub_date']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['user','post_date']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['event']