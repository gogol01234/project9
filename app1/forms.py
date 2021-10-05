
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django import forms
from app1.models import Customer
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _
class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(label = "username", widget = forms.TextInput(attrs = {"class":"form-control"}))
    password1 = forms.CharField(label = "Password", widget = forms.PasswordInput(attrs = {"class":"form-control"}))
    password2 = forms.CharField(label = "Confirm Password (again)", widget = forms.PasswordInput(attrs = {"class":"form-control"}))
    email = forms.CharField(label = "Email", required = True, widget = forms.EmailInput(attrs = {"class":"form-control"}))
    class meta:
        model = User
        fields = "__all__"
class LoginForm(AuthenticationForm):
    username = UsernameField(widget = forms.TextInput(attrs = {"autofocus":True, "class":"form-control"}))
    password = forms.CharField(label = _("Password"), widget = forms.PasswordInput(attrs = {"autocomplete":"current-password", "class":"form-control"}))

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label = "Old Password", strip = False, widget = forms.PasswordInput(attrs = {"autocomplete":"current-password","autofocus":True, "class":"form-control"}))
    new_password1 = forms.CharField(label = "New Password", strip = False, widget = forms.PasswordInput(attrs = {"autocomplete":"new-password","autofocus":True, "class":"form-control"}))
    new_password2 = forms.CharField(label = "Confirm New Password", strip = False, widget = forms.PasswordInput(attrs = {"autocomplete":"new-password","autofocus":True, "class":"form-control"}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label = _("Email"), max_length = 254, widget = forms.EmailInput(
        attrs = {"class":"form-control","autocomplete":"email"}))

        
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label = _("New Password"),strip = False, widget = forms.PasswordInput(attrs = { "autocomplete":"new-password","class":"form-control"}), help_text = password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label = _("Confirm New Password"),strip = False,widget = forms.PasswordInput(attrs = {"class":"form-control"}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "locality", "city", "state", "zipcode"]
        widgets = {"name":forms.TextInput(attrs = {"class":"form-control"}),
        "locality":forms.TextInput(attrs = {"class":"form-control"}),
        "city":forms.TextInput(attrs = {"class":"form-control"}),
        "state":forms.Select(attrs = {"class":"form-control"}),
        "zipcode":forms.NumberInput(attrs = {"class":"form-control"})
        }