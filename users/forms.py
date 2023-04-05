from django import forms
# from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .models import Review
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Contributor, Contribution, Profile,Withdrawal

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False)
    
 
    
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password1',
            'password2',
        ]
    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            self.add_error('email', "Email already exists")
       return self.cleaned_data
    

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    
    class Meta:
        model = User
        fields = [
            'email',
            'username',
        ]

class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = [
            'image',
            'first_name',
            'last_name',
            'bio',
            'phone_number',
        ]


class ContForm(forms.ModelForm):
    CHOICES = [('PU','Public'),('OG','Organizer'), ('AN','Anonymous')]
    class Meta:
        model = Contributor
        fields = [
            'name',
            'phone_number',
            'amount_deposited',
            'audiance',
            'transaction_id',
            'short_message'
        ]
class ContributionForm(forms.ModelForm):
    pass
    class Meta:
        model = Contribution
        fields = [
            'title',
            'category',
            'description',
            'amount_needed',
        ]


class WithdrawalForm(forms.ModelForm):
    pass
    class Meta:
        model = Withdrawal
        fields = [
            'account_number',
            'account_name',
            'bank',
            'amount',
        ]
    