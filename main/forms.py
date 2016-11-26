
from django import forms
from django.forms import ModelForm
from .models import Account

class PasswordForm(forms.ModelForm):
    # Should we restrict the characters?
    password = forms.CharField(widget=forms.PasswordInput,
    				min_length=Account.PASSWORD_MIN_LENGTH,
    				max_length=Account.PASSWORD_MAX_LENGTH,
    				required=True, label="Password")

class RegisterForm(ModelForm):
    class Meta:
        model = Account
        fields = ["first_name", "email", "username", "password", "district_id", "last_name", "gender", "phone_number"]

class LoginForm(PasswordForm):
    remember = forms.BooleanField(required=False)

    def validate_unique(self):
        # Skip uniqueness validation
        pass

class LoginEmailForm(LoginForm):
    class Meta:
        model = Account
        fields = ["email", "password"]

class LoginUsernameForm(ModelForm):
    class Meta:
        model = Account
        fields = ["username", "password"]