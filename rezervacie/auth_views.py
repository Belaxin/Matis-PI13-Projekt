from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import LoginForm, RegisterForm, UserCreateForm


def is_admin(user):
    return user.is_staff


# ── AUTH ───────────────────────────────────────────────────────────────────

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        u = form.get_user()
        login(request, u)
        return redirect("admin_dashboard" if u.is_staff else "index")
    return render(request, "rezervacie/login.html", {"form": form})


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("index")
    return render(request, "rezervacie/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


# ── ADMIN DASHBOARD ────────────────────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    from .models import Reservation, Room, Equipment
    return render(request, "rezervacie/admin_dashboard.html", {
        "users":        User.objects.all(),
        "reservations": Reservation.objects.select_related("pouzivatelRezervacie", "miestnostRezervacie").order_by("datumRezervacie", "casOd"),
        "rooms":        Room.objects.all(),
        "equipment":    Equipment.objects.all(),
    })


# ── ADMIN – USER MANAGEMENT ────────────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def admin_user_create(request):
    form = UserCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Používateľ bol vytvorený.")
        return redirect("admin_dashboard")
    return render(request, "rezervacie/admin_user_form.html", {"form": form, "title": "Nový používateľ"})


@login_required
@user_passes_test(is_admin)
def admin_user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UserCreateForm(request.POST or None, instance=user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Používateľ bol upravený.")
        return redirect("admin_dashboard")
    return render(request, "rezervacie/admin_user_form.html", {"form": form, "title": "Upraviť používateľa"})


@login_required
@user_passes_test(is_admin)
def admin_user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        messages.success(request, "Používateľ bol odstránený.")
        return redirect("admin_dashboard")
    return render(request, "rezervacie/confirm_delete.html", {"object": user, "type": "používateľa"})


# ── ADMIN – RESERVATION MANAGEMENT ────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def admin_reservation_delete(request, pk):
    from .models import Reservation
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == "POST":
        reservation.delete()
        messages.success(request, "Rezervácia bola odstránená.")
        return redirect("admin_dashboard")
    return render(request, "rezervacie/confirm_delete.html", {"object": reservation, "type": "rezerváciu"})