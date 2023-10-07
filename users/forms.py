from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

###############################################
#              Register & Login               #
###############################################

class RegisterForm(UserCreationForm):
    email = forms.CharField()
    email_code = forms.CharField()
    class Meta:
        model = User
        fields = ("username", "email", "email_code", "password1", "password2")
        
        
class LoginForm(forms.Form):
    login_email = forms.CharField()
    login_password = forms.CharField()


