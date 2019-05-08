from django import forms
from .models import Profile,Event,Ticket,Tpayment,Payment

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
        model = Ticket
        exclude = ['event']

class TpaymentForm(forms.ModelForm):
    class Meta:
        model = Tpayment
        exclude = ['event','ticket_category']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['event','tpayment', 'amount', 'number_of_tickets']