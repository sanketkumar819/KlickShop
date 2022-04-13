from django import forms
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm,PasswordResetForm, AuthenticationForm,UsernameField,PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer, Product, OrderPlaced, Cart

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm  password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, label='Enter your email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_("password"),strip=False ,widget=forms.TextInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))
    
    
class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old password"),strip=False ,widget=forms.TextInput(attrs={'autofocus':True,'autocomplete':'current-password', 'class':'form-control'}))
    new_password1 = forms.CharField(label=_("New password"),strip=False ,widget=forms.TextInput(attrs={'autocomplete':'current-password', 'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm password"),strip=False ,widget=forms.TextInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))
    
    
    
class UserPasswordResetForm(PasswordResetForm): 
    email = forms.EmailField(label=_("Email"),max_length=254 ,widget=forms.EmailInput(attrs={'autocomplete':'Email', 'class':'form-control'}))
    
    
    
    
class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New password"),strip=False ,widget=forms.TextInput(attrs={'autofocus':True,'autocomplete':'current-password', 'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm password"),strip=False ,widget=forms.TextInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','zipcode','state']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),'locality':forms.TextInput(attrs={'class':'form-control'}),'city':forms.TextInput(attrs={'class':'form-control'}),'state':forms.Select(attrs={'class':'form-control'}),'zipcode':forms.NumberInput(attrs={'class':'form-control'})}