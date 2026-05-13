"""
REST API using Django's built-in JsonResponse — no extra libraries needed.
JsonResponse takes a Python dict and serializes it to JSON automatically.

These endpoints return data that could be consumed by a frontend JS fetch(),
a mobile app, or another service. They're separate from the HTML views.
"""

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

from .models import Room, Reservation


# ── ROOMS ──────────────────────────────────────────────────────────────────

@require_GET  # returns 405 Method Not Allowed for POST/PUT/DELETE
@login_required
def api_room_list(request):
    """
    GET /api/miestnosti/
    Optional filters: ?typ=UC  ?search=fyzika
    """
    rooms = Room.objects.all()

    typ    = request.GET.get("typ")
    search = request.GET.get("search", "").strip()

    if typ:
        rooms = rooms.filter(typMiestnosti=typ)
    if search:
        rooms = rooms.filter(nazovMiestnosti__icontains=search)

    data = [
        {
            "id":       room.pk,
            "nazov":    room.nazovMiestnosti,
            "cislo":    room.cisloMiestnosti,
            "kapacita": room.kapacitaMiestnosti,
            "typ":      room.get_typMiestnosti_display(),  # human-readable label
            "typ_kod":  room.typMiestnosti,
            "popis":    room.popisMiestnosti or "",
        }
        for room in rooms
    ]

    return JsonResponse({"count": len(data), "miestnosti": data})


@require_GET
@login_required
def api_room_detail(request, pk):
    """
    GET /api/miestnosti/<pk>/
    Returns room info + all its reservations.
    """
    try:
        room = Room.objects.get(pk=pk)
    except Room.DoesNotExist:
        return JsonResponse({"error": "Miestnosť nenájdená."}, status=404)

    rezervacie = Reservation.objects.filter(
        miestnostRezervacie=room
    ).select_related("pouzivatelRezervacie")

    # date filter
    datum = request.GET.get("datum")
    if datum:
        rezervacie = rezervacie.filter(datumRezervacie=datum)

    rezervacie_data = [
        {
            "id":         r.pk,
            "datum":      str(r.datumRezervacie),
            "casOd":      str(r.casOd),
            "casDo":      str(r.casDo),
            "ucel":       r.ucelRezervacie,
            "pouzivatel": r.pouzivatelRezervacie.username if r.pouzivatelRezervacie else None,
        }
        for r in rezervacie
    ]

    return JsonResponse({
        "id":         room.pk,
        "nazov":      room.nazovMiestnosti,
        "cislo":      room.cisloMiestnosti,
        "kapacita":   room.kapacitaMiestnosti,
        "typ":        room.get_typMiestnosti_display(),
        "popis":      room.popisMiestnosti or "",
        "rezervacie": rezervacie_data,
    })


# ── RESERVATIONS ───────────────────────────────────────────────────────────

@require_GET
@login_required
def api_reservation_list(request):
    """
    GET /api/rezervacie/
    Admins see all. Regular users only see their own.
    Optional filters: ?datum=2025-01-01  ?miestnost=3
    """
    if request.user.is_staff:
        rezervacie = Reservation.objects.select_related("miestnostRezervacie", "pouzivatelRezervacie")
    else:
        rezervacie = Reservation.objects.filter(
            pouzivatelRezervacie=request.user
        ).select_related("miestnostRezervacie")

    datum      = request.GET.get("datum")
    miestnost  = request.GET.get("miestnost")

    if datum:
        rezervacie = rezervacie.filter(datumRezervacie=datum)
    if miestnost:
        rezervacie = rezervacie.filter(miestnostRezervacie_id=miestnost)

    rezervacie = rezervacie.order_by("datumRezervacie", "casOd")

    data = [
        {
            "id":         r.pk,
            "datum":      str(r.datumRezervacie),
            "casOd":      str(r.casOd),
            "casDo":      str(r.casDo),
            "ucel":       r.ucelRezervacie,
            "miestnost":  r.miestnostRezervacie.nazovMiestnosti if r.miestnostRezervacie else None,
            "pouzivatel": r.pouzivatelRezervacie.username if r.pouzivatelRezervacie else None,
        }
        for r in rezervacie
    ]

    return JsonResponse({"count": len(data), "rezervacie": data})


@require_GET
@login_required
def api_reservation_detail(request, pk):
    """GET /api/rezervacie/<pk>/"""
    try:
        r = Reservation.objects.select_related(
            "miestnostRezervacie", "pouzivatelRezervacie"
        ).get(pk=pk)
    except Reservation.DoesNotExist:
        return JsonResponse({"error": "Rezervácia nenájdená."}, status=404)

    # non-owners can't access other people's reservations via API either
    if not request.user.is_staff and r.pouzivatelRezervacie != request.user:
        return JsonResponse({"error": "Prístup zamietnutý."}, status=403)

    vybavenie = [
        {
            "nazov":      re.vybavenie.nazovVybavenia,
            "pocetKusov": re.pocetKusov,
            "poznamka":   re.poznamka or "",
        }
        for re in r.reservationequipment_set.select_related("vybavenie")
    ]

    return JsonResponse({
        "id":         r.pk,
        "datum":      str(r.datumRezervacie),
        "casOd":      str(r.casOd),
        "casDo":      str(r.casDo),
        "ucel":       r.ucelRezervacie,
        "miestnost":  r.miestnostRezervacie.nazovMiestnosti if r.miestnostRezervacie else None,
        "pouzivatel": r.pouzivatelRezervacie.username if r.pouzivatelRezervacie else None,
        "vybavenie":  vybavenie,
    })
