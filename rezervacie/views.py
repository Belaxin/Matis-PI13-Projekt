from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from datetime import date

from .models import Room, Equipment, Reservation, ReservationEquipment
from .forms import (
    LoginForm, RegisterForm, UserCreateForm,
    ReservationForm, ReservationEquipmentForm,
    RoomForm, EquipmentForm,
)


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


# ── INDEX ──────────────────────────────────────────────────────────────────

@login_required
def index(request):
    from django.utils import timezone
    today = timezone.localdate()  # Get today's date
    print("DEBUG: Today's date:", today)  # Debug today's date

    rezervacie = Reservation.objects.filter(
        datumRezervacie=today
    ).select_related("miestnostRezervacie", "pouzivatelRezervacie").order_by("casOd")
    print("DEBUG: Reservations for today:", rezervacie)  # Debug queryset

    if not rezervacie.exists():
        # Fallback to system date if timezone date doesn't match
        today_alt = date.today()
        print("DEBUG: Fallback to system date:", today_alt)  # Debug fallback date
        if today_alt != today:
            rezervacie = Reservation.objects.filter(
                datumRezervacie=today_alt
            ).select_related("miestnostRezervacie", "pouzivatelRezervacie").order_by("casOd")
            today = today_alt
            print("DEBUG: Reservations for fallback date:", rezervacie)  # Debug fallback queryset

    return render(request, "rezervacie/index.html", {
        "rezervacie": rezervacie,
        "today": today,
        "rooms_count": Room.objects.count(),
        "total_count": Reservation.objects.count(),
    })


# ── ADMIN ──────────────────────────────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, "rezervacie/admin_dashboard.html", {
        "users":        User.objects.all(),
        "reservations": Reservation.objects.select_related("pouzivatelRezervacie", "miestnostRezervacie").order_by("datumRezervacie", "casOd"),
        "rooms":        Room.objects.all(),
        "equipment":    Equipment.objects.all(),
    })


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


@login_required
@user_passes_test(is_admin)
def admin_reservation_delete(request, pk):
    rezervacia = get_object_or_404(Reservation, pk=pk)
    if request.method == "POST":
        rezervacia.delete()
        messages.success(request, "Rezervácia bola odstránená.")
        return redirect("admin_dashboard")
    return render(request, "rezervacie/confirm_delete.html", {"object": rezervacia, "type": "rezerváciu"})


# ── RESERVATIONS ───────────────────────────────────────────────────────────

@login_required
def reservation_list(request):
    # everyone sees all reservations
    rezervacie = Reservation.objects.select_related("pouzivatelRezervacie", "miestnostRezervacie")

    datum   = request.GET.get("datum")
    room_id = request.GET.get("miestnost")
    search  = request.GET.get("search", "").strip()

    if datum:
        rezervacie = rezervacie.filter(datumRezervacie=datum)
    if room_id:
        rezervacie = rezervacie.filter(miestnostRezervacie_id=room_id)
    if search:
        rezervacie = rezervacie.filter(ucelRezervacie__icontains=search)

    rezervacie = rezervacie.order_by("datumRezervacie", "casOd")

    return render(request, "rezervacie/reservation_list.html", {
        "rezervacie": rezervacie,
        "rooms": Room.objects.all(),
    })


@login_required
def reservation_detail(request, pk):
    rezervacia = get_object_or_404(Reservation, pk=pk)
    vybavenie = ReservationEquipment.objects.filter(rezervacia=rezervacia).select_related("vybavenie")
    form = ReservationEquipmentForm()
    return render(request, "rezervacie/reservation_detail.html", {
        "rezervacia": rezervacia,
        "vybavenie": vybavenie,
        "form": form,
    })


@login_required
def reservation_create(request):
    form = ReservationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        rezervacia = form.save(commit=False)
        rezervacia.pouzivatelRezervacie = request.user  # attach logged-in user
        rezervacia.save()
        messages.success(request, "Rezervácia bola vytvorená.")
        return redirect("reservation_detail", pk=rezervacia.pk)
    return render(request, "rezervacie/reservation_form.html", {
        "form": form,
        "title": "Nová rezervácia",
    })


@login_required
def reservation_edit(request, pk):
    rezervacia = get_object_or_404(Reservation, pk=pk)

    # only owner or admin can edit
    if not request.user.is_staff and rezervacia.pouzivatelRezervacie != request.user:
        messages.error(request, "Nemáš oprávnenie upraviť túto rezerváciu.")
        return redirect("reservation_list")

    form = ReservationForm(request.POST or None, instance=rezervacia)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Rezervácia bola upravená.")
        return redirect("reservation_detail", pk=pk)
    return render(request, "rezervacie/reservation_form.html", {
        "form": form,
        "title": "Upraviť rezerváciu",
    })


@login_required
def reservation_cancel(request, pk):
    rezervacia = get_object_or_404(Reservation, pk=pk)
 
    if not request.user.is_staff and rezervacia.pouzivatelRezervacie != request.user:
        messages.error(request, "Nemáš oprávnenie zrušiť túto rezerváciu.")
        return redirect("reservation_list")
 
    if request.method == "POST":
        rezervacia.delete()
        messages.success(request, "Rezervácia bola zrušená.")
        return redirect("reservation_list")
 
    # fallback if somehow accessed via GET
    return redirect("reservation_detail", pk=pk)
 


# ── EQUIPMENT ASSIGNMENT (M:N) ─────────────────────────────────────────────

@login_required
def add_equipment(request, pk):
    """
    Adds a row to ReservationEquipment (the through table).
    pk here is the reservation's pk.
    """
    rezervacia = get_object_or_404(Reservation, pk=pk)

    if not request.user.is_staff and rezervacia.pouzivatelRezervacie != request.user:
        messages.error(request, "Nemáš oprávnenie.")
        return redirect("reservation_detail", pk=pk)

    form = ReservationEquipmentForm(request.POST)
    if form.is_valid():
        polozka = form.save(commit=False)
        polozka.rezervacia = rezervacia  # link to the reservation
        polozka.save()
        messages.success(request, "Vybavenie bolo priradené.")
    return redirect("reservation_detail", pk=pk)


@login_required
def remove_equipment(request, pk):
    """pk here is the ReservationEquipment row's pk, not the reservation."""
    polozka = get_object_or_404(ReservationEquipment, pk=pk)
    rezervacia_pk = polozka.rezervacia.pk

    if not request.user.is_staff and polozka.rezervacia.pouzivatelRezervacie != request.user:
        messages.error(request, "Nemáš oprávnenie.")
        return redirect("reservation_detail", pk=rezervacia_pk)

    if request.method == "POST":
        polozka.delete()
        messages.success(request, "Vybavenie bolo odobraté.")
    return redirect("reservation_detail", pk=rezervacia_pk)


# ── ROOMS ──────────────────────────────────────────────────────────────────

@login_required
def room_list(request):
    rooms = Room.objects.all()
    typ    = request.GET.get("typ")
    search = request.GET.get("search", "").strip()
    if typ:
        rooms = rooms.filter(typMiestnosti=typ)
    if search:
        rooms = rooms.filter(
            Q(nazovMiestnosti__icontains=search) | Q(cisloMiestnosti__icontains=search)
        )
    return render(request, "rezervacie/room_list.html", {
        "rooms": rooms,
        "typy": Room.Typ.choices,
    })


@login_required
def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    rezervacie = Reservation.objects.filter(miestnostRezervacie=room).order_by("datumRezervacie", "casOd")
    datum = request.GET.get("datum")
    if datum:
        rezervacie = rezervacie.filter(datumRezervacie=datum)
    return render(request, "rezervacie/room_detail.html", {"room": room, "rezervacie": rezervacie})


@login_required
@user_passes_test(is_admin)
def room_create(request):
    form = RoomForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Miestnosť bola vytvorená.")
        return redirect("room_list")
    return render(request, "rezervacie/room_form.html", {"form": form, "title": "Nová miestnosť"})


@login_required
@user_passes_test(is_admin)
def room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)
    form = RoomForm(request.POST or None, instance=room)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Miestnosť bola upravená.")
        return redirect("room_detail", pk=pk)
    return render(request, "rezervacie/room_form.html", {"form": form, "title": "Upraviť miestnosť"})


@login_required
@user_passes_test(is_admin)
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == "POST":
        room.delete()
        messages.success(request, "Miestnosť bola odstránená.")
        return redirect("room_list")
    return render(request, "rezervacie/confirm_delete.html", {"object": room, "type": "miestnosť"})


# ── EQUIPMENT ──────────────────────────────────────────────────────────────

@login_required
def equipment_list(request):
    equipment = Equipment.objects.all()
    search = request.GET.get("search", "").strip()
    if search:
        equipment = equipment.filter(
            Q(nazovVybavenia__icontains=search) | Q(typVybavenia__icontains=search)
        )
    return render(request, "rezervacie/equipment_list.html", {"equipment": equipment})


@login_required
@user_passes_test(is_admin)
def equipment_create(request):
    form = EquipmentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Vybavenie bolo pridané.")
        return redirect("equipment_list")
    return render(request, "rezervacie/equipment_form.html", {"form": form, "title": "Nové vybavenie"})


@login_required
@user_passes_test(is_admin)
def equipment_edit(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    form = EquipmentForm(request.POST or None, instance=equipment)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Vybavenie bolo upravené.")
        return redirect("equipment_list")
    return render(request, "rezervacie/equipment_form.html", {"form": form, "title": "Upraviť vybavenie"})


@login_required
@user_passes_test(is_admin)
def equipment_delete(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == "POST":
        equipment.delete()
        messages.success(request, "Vybavenie bolo odstránené.")
        return redirect("equipment_list")
    return render(request, "rezervacie/confirm_delete.html", {"object": equipment, "type": "vybavenie"})
