from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


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
        if cleaned_data.get("password") != cleaned_data.get("password2"):
            raise forms.ValidationError("Heslá sa nezhodujú.")
        return cleaned_data

    def save(self, commit=True):
        return User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )


class UserCreateForm(forms.ModelForm):
    """
    Used by admin to create/edit users.
    is_staff checkbox lets admin promote a user to admin directly from the site.
    password field is optional on edit — leave blank to keep existing password.
    """
    password  = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class": "form-control"}),
                                help_text="Nechaj prázdne ak nechceš meniť heslo.")
    password2 = forms.CharField(required=False, label="Potvrď heslo",
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model  = User
        fields = ["username", "email", "first_name", "last_name", "is_staff"]
        widgets = {
            "username":   forms.TextInput(attrs={"class": "form-control"}),
            "email":      forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name":  forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "is_staff": "Admin práva",
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("password2")
        if p1 and p1 != p2:
            raise forms.ValidationError("Heslá sa nezhodujú.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)  # set_password hashes it — same as create_user does internally
        if commit:
            user.save()
        return user