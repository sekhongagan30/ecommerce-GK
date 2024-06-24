from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile
from core.models import Address

class UserRegisterationForm(UserCreationForm): # can allso use forms.ModelForm in place of UserCreationForms
    # if we don't specify fields in below style, then forms will make default widgets for that model specified in Meta
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': "Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Confirm Password"}))
    #############################
    # with UserCreationForm: detailing mai fields aate hai, in addition to fields, password and confirm password
    # also info k password shud be proper etc
    # with forms.ModelForm sirf fields hi show hongi
    class Meta:
        model = User
        fields = ['username', 'email'] # write model col names here, rest django forms will add up

class ProfileForm(forms.ModelForm):
    # full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Full Name"}))
    # # image = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Full Name"}))
    # bio = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': "Bio"}))
    # phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Phone"}))
    class Meta:
        model = Profile
        fields = ['full_name', 'image', 'bio', 'phone']

class AddressForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Address"}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Mobile"}))

    class Meta:
        model = Address
        fields = ['address', 'mobile']