from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your mobile number or username',
        'id': 'login_username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your secure password',
        'id': 'login_password'
    }))

class FarmerRegisterForm(forms.ModelForm):
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'e.g. 9812044550'
    }))
    state = forms.CharField(required=True, initial='Haryana', widget=forms.TextInput(attrs={'class': 'form-control'}))
    district = forms.CharField(required=True, initial='Karnal', widget=forms.TextInput(attrs={'class': 'form-control'}))
    landholding_acres = forms.DecimalField(initial=2.5, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose username or mobile'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }

class BuyerRegisterForm(forms.ModelForm):
    business_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Shiva Agro Traders'}))
    category = forms.ChoiceField(choices=[
        ('LOCAL_TRADER', 'Local Mandi Trader'),
        ('WHOLESALER', 'Wholesale Commission Agent'),
        ('FOOD_PROCESSOR', 'Food Processing Mill'),
        ('INSTITUTIONAL', 'Institutional Buyer')
    ], widget=forms.Select(attrs={'class': 'form-select'}))
    mandi_license = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'APMC License Number'}))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'phone_number', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Person'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
