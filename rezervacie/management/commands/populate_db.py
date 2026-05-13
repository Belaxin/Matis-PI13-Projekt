"""
Run this with: python manage.py shell < populate_db.py

This script creates realistic school reservation data.
Superuser: admin / admin
Regular users: password = their username (e.g. jnovak / jnovak)
"""

from django.contrib.auth.models import User
from rezervacie.models import Room, Equipment, Reservation, ReservationEquipment
from datetime import date, time

# ── CLEAN SLATE ────────────────────────────────────────────────────────────
ReservationEquipment.objects.all().delete()
Reservation.objects.all().delete()
Equipment.objects.all().delete()
Room.objects.all().delete()
User.objects.all().delete()

# ── SUPERUSER ──────────────────────────────────────────────────────────────
admin = User.objects.create_superuser(
    username="admin",
    password="admin",
    email="admin@skola.sk",
    first_name="Admin",
    last_name="Systém",
)

# ── REGULAR USERS ──────────────────────────────────────────────────────────
users_data = [
    ("jnovak",    "Ján",      "Novák",      "jnovak@skola.sk"),
    ("mhorkova",  "Mária",    "Horková",    "mhorkova@skola.sk"),
    ("pkubica",   "Peter",    "Kubica",     "pkubica@skola.sk"),
    ("zkovacova", "Zuzana",   "Kováčová",   "zkovacova@skola.sk"),
    ("tbalog",    "Tomáš",    "Balog",      "tbalog@skola.sk"),
]

users = {}
for username, first, last, email in users_data:
    u = User.objects.create_user(
        username=username,
        password=username,  # password = username
        email=email,
        first_name=first,
        last_name=last,
    )
    users[username] = u

# ── ROOMS ──────────────────────────────────────────────────────────────────
rooms_data = [
    ("Učebňa A1",       101, 30, "UC", "Štandardná učebňa s interaktívnou tabuľou."),
    ("Učebňa A2",       102, 25, "UC", "Štandardná učebňa s projektorom."),
    ("Počítačová sála", 201, 20, "LA", "Vybavená 20 PC stanicami a rýchlym internetom."),
    ("Fyzikálne lab.",  202, 18, "LA", "Laboratórium pre fyzikálne experimenty."),
    ("Chemické lab.",   203, 16, "LA", "Laboratórium s digestorom a bezpečnostným vybavením."),
    ("Telocvičňa",      1,  0, "TE", "Veľká telocvičňa s parketovou podlahou."),
    ("Knižnica",        301, 40, "KN", "Školská knižnica s čitárňou."),
    ("Zborovňa",        302, 20, "KA", "Zasadačka pre pedagogický zbor."),
]

rooms = {}
for nazov, cislo, kapacita, typ, popis in rooms_data:
    r = Room.objects.create(
        nazovMiestnosti=nazov,
        cisloMiestnosti=cislo,
        kapacitaMiestnosti=kapacita,
        typMiestnosti=typ,
        popisMiestnosti=popis,
    )
    rooms[nazov] = r

# ── EQUIPMENT ──────────────────────────────────────────────────────────────
equipment_data = [
    ("Projektor Epson",     "EL", "Prenosný projektor 4000 lúmenov."),
    ("Notebook Dell",       "EL", "Učiteľský notebook s Windows 11."),
    ("Interaktívna tabuľa", "EL", "Smart Board 75 palcov."),
    ("Mikrofón",            "EL", "Bezdrôtový mikrofón pre prezentácie."),
    ("Stoličky skladacie",  "NA", "Skladacie stoličky pre extra kapacitu."),
    ("Stôl skladací",       "NA", "Ľahký skladací stôl 180cm."),
    ("Volejbalová sieť",    "SP", "Súprava pre volejbal vrátane stĺpikov."),
    ("Basketbalové lopty",  "SP", "Sada 6 basketbalových lôpt."),
]

equipment = {}
for nazov, typ, popis in equipment_data:
    e = Equipment.objects.create(
        nazovVybavenia=nazov,
        typVybavenia=typ,
        popis=popis,
    )
    equipment[nazov] = e

# ── RESERVATIONS ───────────────────────────────────────────────────────────
reservations_data = [
    # (user, room, date, time_from, time_to, ucel)
    ("jnovak",    "Učebňa A1",       date(2025, 6,  2), time(8,  0), time(9,  30), "Matematika – 3.A"),
    ("mhorkova",  "Učebňa A2",       date(2025, 6,  2), time(9,  0), time(10, 30), "Slovenský jazyk – 2.B"),
    ("pkubica",   "Počítačová sála", date(2025, 6,  2), time(10, 0), time(11, 30), "Informatika – 4.A"),
    ("jnovak",    "Učebňa A1",       date(2025, 6,  2), time(11, 0), time(12, 30), "Matematika – 4.B"),
    ("zkovacova", "Fyzikálne lab.",  date(2025, 6,  2), time(8,  0), time(10,  0), "Fyzika – merania"),
    ("tbalog",    "Telocvičňa",      date(2025, 6,  2), time(13, 0), time(15,  0), "Telesná výchova – 1.A"),
    ("mhorkova",  "Knižnica",        date(2025, 6,  3), time(9,  0), time(11,  0), "Čitateľský krúžok"),
    ("pkubica",   "Počítačová sála", date(2025, 6,  3), time(8,  0), time(10,  0), "Programovanie – 3.B"),
    ("jnovak",    "Zborovňa",        date(2025, 6,  3), time(14, 0), time(15,  0), "Porada kabinetu matematiky"),
    ("zkovacova", "Chemické lab.",   date(2025, 6,  4), time(9,  0), time(11,  0), "Chémia – pokusy 2.A"),
    ("tbalog",    "Telocvičňa",      date(2025, 6,  4), time(13, 0), time(15,  0), "Volejbalový turnaj"),
    ("mhorkova",  "Učebňa A1",       date(2025, 6,  5), time(8,  0), time(9,  30), "Literatúra – 3.A"),
    ("pkubica",   "Počítačová sála", date(2025, 6,  5), time(10, 0), time(12,  0), "Testovanie – 4.A"),
    ("admin",     "Zborovňa",        date(2025, 6,  5), time(15, 0), time(16,  0), "Pedagogická rada"),
]

rezervacie = {}
for username, room_name, datum, cas_od, cas_do, ucel in reservations_data:
    user = users.get(username) or admin
    r = Reservation.objects.create(
        datumRezervacie=datum,
        casOd=cas_od,
        casDo=cas_do,
        ucelRezervacie=ucel,
        miestnostRezervacie=rooms[room_name],
        pouzivatelRezervacie=user,
    )
    rezervacie[(username, ucel)] = r

# ── EQUIPMENT ASSIGNMENTS ──────────────────────────────────────────────────
ReservationEquipment.objects.create(
    rezervacia=rezervacie[("pkubica", "Informatika – 4.A")],
    vybavenie=equipment["Projektor Epson"],
    pocetKusov=1,
    poznamka="Premietanie prezentácie",
)
ReservationEquipment.objects.create(
    rezervacia=rezervacie[("pkubica", "Informatika – 4.A")],
    vybavenie=equipment["Notebook Dell"],
    pocetKusov=1,
)
ReservationEquipment.objects.create(
    rezervacia=rezervacie[("tbalog", "Volejbalový turnaj")],
    vybavenie=equipment["Volejbalová sieť"],
    pocetKusov=1,
)
ReservationEquipment.objects.create(
    rezervacia=rezervacie[("tbalog", "Volejbalový turnaj")],
    vybavenie=equipment["Basketbalové lopty"],
    pocetKusov=6,
    poznamka="Záložné lopty pre rozcvičku",
)
ReservationEquipment.objects.create(
    rezervacia=rezervacie[("admin", "Pedagogická rada")],
    vybavenie=equipment["Projektor Epson"],
    pocetKusov=1,
)
ReservationEquipment.objects.create(
    rezervacia=rezervacie[("admin", "Pedagogická rada")],
    vybavenie=equipment["Stoličky skladacie"],
    pocetKusov=10,
    poznamka="Pre pozvaných rodičov",
)
ReservationEquipment.objects.create(
    rezervacia=rezervacie[("jnovak", "Porada kabinetu matematiky")],
    vybavenie=equipment["Interaktívna tabuľa"],
    pocetKusov=1,
)

print("✅ Databáza naplnená.")
print(f"   Používatelia: {User.objects.count()}")
print(f"   Miestnosti:   {Room.objects.count()}")
print(f"   Vybavenie:    {Equipment.objects.count()}")
print(f"   Rezervácie:   {Reservation.objects.count()}")
print()
print("Prihlasovacie údaje:")
print("  admin     / admin")
for username, *_ in users_data:
    print(f"  {username:<12} / {username}")
