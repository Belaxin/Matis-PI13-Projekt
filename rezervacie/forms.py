from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


# AuthenticationForm is Django's built-in login form — no need to reinvent it.
# It handles username/password validation automatically.
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Meno"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Heslo"}))


class RegisterForm(forms.ModelForm):
    password  = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Potvrď heslo", widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model  = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email":    forms.EmailInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Heslá sa nezhodujú.")
        return cleaned_data

    def save(self, commit=True):
        # create_user() hashes the password — never skip this
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )
        return user
