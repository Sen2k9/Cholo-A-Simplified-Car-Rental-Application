from django.contrib.auth.models import User
from .models import Ride, Customer, Vehicle, Driver
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserForm(forms.ModelForm):
#class UserForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (

            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        )

    def save(self, commit=True):

        user = super(UserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (

            'email',
            'first_name',
            'last_name'
        )


class RideForm(forms.ModelForm):
    starting_location = forms.CharField( max_length=500, required=False)
    destination = forms.CharField(max_length=500, required=False)
    starting_time = forms.CharField(max_length=500, required=False)
    ending_time = forms.CharField(max_length=500, required=False)
    fare = forms.IntegerField(required=False)
    
    class Meta:
        model = Ride
        fields = ('starting_location', 'destination', 'starting_time', 'ending_time','fare',)
        #included comma at the last to make it tuple
