from django.forms import ModelForm, Form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *


class UserRegistration(UserCreationForm):
    rating_text = models.CharField(max_length=120)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PostRequestForm(forms.ModelForm):
    class Meta:
        model = BuyerPostRequest
        fields = '__all__'
    
class ExtendedUserForm(forms.ModelForm):
    class Meta:
        model = SellerAccount
        fields = "__all__"

class SellerSubmitForm(forms.ModelForm):
    class Meta:
        model = SellerSubmit
        fields = "__all__"