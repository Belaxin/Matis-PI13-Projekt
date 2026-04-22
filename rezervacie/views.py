from django.shortcuts import render


# Each view gets a request, returns a response.
# render(request, "template_path", context_dict)
# context = variables you want available in the HTML — fill these in later when models exist.


def index(request):
    return render(request, "rezervacie/index.html", {})


# ── ROOMS ──────────────────────────────────────────────────────────────────

def room_list(request):
    return render(request, "rezervacie/room_list.html", {})

def room_detail(request, pk):
    return render(request, "rezervacie/room_detail.html", {})

def room_create(request):
    return render(request, "rezervacie/room_form.html", {})

def room_edit(request, pk):
    return render(request, "rezervacie/room_form.html", {})

def room_delete(request, pk):
    return render(request, "rezervacie/confirm_delete.html", {})


# ── rezervacie ───────────────────────────────────────────────────────────

def reservation_list(request):
    return render(request, "rezervacie/reservation_list.html", {})

def reservation_detail(request, pk):
    return render(request, "rezervacie/reservation_detail.html", {})

def reservation_create(request):
    return render(request, "rezervacie/reservation_form.html", {})

def reservation_edit(request, pk):
    return render(request, "rezervacie/reservation_form.html", {})

def reservation_cancel(request, pk):
    return render(request, "rezervacie/confirm_delete.html", {})


# ── EQUIPMENT ──────────────────────────────────────────────────────────────

def equipment_list(request):
    return render(request, "rezervacie/equipment_list.html", {})

def equipment_create(request):
    return render(request, "rezervacie/equipment_form.html", {})

def equipment_edit(request, pk):
    return render(request, "rezervacie/equipment_form.html", {})

def equipment_delete(request, pk):
    return render(request, "rezervacie/confirm_delete.html", {})
