from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Reservation, ReservationEquipment, Room, Equipment


# ── AUTH ───────────────────────────────────────────────────────────────────

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Používateľské meno",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Meno"})
    )
    password = forms.CharField(
        label="Heslo",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Heslo"})
    )


class RegisterForm(forms.ModelForm):
    password  = forms.CharField(
        label="Heslo",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Potvrď heslo",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model  = User
        fields = ["username", "email"]
        labels = {
            "username": "Používateľské meno",
            "email":    "E-mail",
        }
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
    password  = forms.CharField(
        label="Heslo",
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Nechaj prázdne ak nechceš meniť heslo."
    )
    password2 = forms.CharField(
        label="Potvrď heslo",
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model  = User
        fields = ["username", "email", "first_name", "last_name", "is_staff"]
        labels = {
            "username":   "Používateľské meno",
            "email":      "E-mail",
            "first_name": "Meno",
            "last_name":  "Priezvisko",
            "is_staff":   "Admin práva",
        }
        widgets = {
            "username":   forms.TextInput(attrs={"class": "form-control"}),
            "email":      forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name":  forms.TextInput(attrs={"class": "form-control"}),
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
        if self.cleaned_data.get("password"):
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# ── RESERVATION ────────────────────────────────────────────────────────────

class ReservationForm(forms.ModelForm):
    class Meta:
        model  = Reservation
        fields = ["datumRezervacie", "casOd", "casDo", "ucelRezervacie", "miestnostRezervacie"]
        labels = {
            "datumRezervacie":     "Dátum",
            "casOd":               "Čas od",
            "casDo":               "Čas do",
            "ucelRezervacie":      "Účel rezervácie",
            "miestnostRezervacie": "Miestnosť",
        }
        widgets = {
            "datumRezervacie":     forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "casOd":               forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "casDo":               forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "ucelRezervacie":      forms.TextInput(attrs={"class": "form-control"}),
            "miestnostRezervacie": forms.Select(attrs={"class": "form-select"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        instance = self.instance
        instance.datumRezervacie     = cleaned_data.get("datumRezervacie")
        instance.casOd               = cleaned_data.get("casOd")
        instance.casDo               = cleaned_data.get("casDo")
        instance.miestnostRezervacie = cleaned_data.get("miestnostRezervacie")
        try:
            instance.clean()
        except forms.ValidationError as e:
            raise e
        return cleaned_data


# ── EQUIPMENT ASSIGNMENT ───────────────────────────────────────────────────

class ReservationEquipmentForm(forms.ModelForm):
    class Meta:
        model  = ReservationEquipment
        fields = ["vybavenie", "pocetKusov", "poznamka"]
        labels = {
            "vybavenie":  "Vybavenie",
            "pocetKusov": "Počet kusov",
            "poznamka":   "Poznámka",
        }
        widgets = {
            "vybavenie":  forms.Select(attrs={"class": "form-select"}),
            "pocetKusov": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "poznamka":   forms.TextInput(attrs={"class": "form-control"}),
        }


# ── ROOM ───────────────────────────────────────────────────────────────────

class RoomForm(forms.ModelForm):
    class Meta:
        model  = Room
        fields = ["nazovMiestnosti", "cisloMiestnosti", "kapacitaMiestnosti", "typMiestnosti", "popisMiestnosti"]
        labels = {
            "nazovMiestnosti":    "Názov miestnosti",
            "cisloMiestnosti":    "Číslo miestnosti",
            "kapacitaMiestnosti": "Kapacita",
            "typMiestnosti":      "Typ miestnosti",
            "popisMiestnosti":    "Popis",
        }
        widgets = {
            "nazovMiestnosti":    forms.TextInput(attrs={"class": "form-control"}),
            "cisloMiestnosti":    forms.NumberInput(attrs={"class": "form-control"}),
            "kapacitaMiestnosti": forms.NumberInput(attrs={"class": "form-control"}),
            "typMiestnosti":      forms.Select(attrs={"class": "form-select"}),
            "popisMiestnosti":    forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


# ── EQUIPMENT ──────────────────────────────────────────────────────────────

class EquipmentForm(forms.ModelForm):
    class Meta:
        model  = Equipment
        fields = ["nazovVybavenia", "typVybavenia", "popis"]
        labels = {
            "nazovVybavenia": "Názov vybavenia",
            "typVybavenia":   "Typ vybavenia",
            "popis":          "Popis",
        }
        widgets = {
            "nazovVybavenia": forms.TextInput(attrs={"class": "form-control"}),
            "typVybavenia":   forms.Select(attrs={"class": "form-select"}),
            "popis":          forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
