from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rezervacie.models import Room, Equipment, Reservation, ReservationEquipment
from datetime import date, time


class Command(BaseCommand):
    help = "Populate database with sample data"

    def handle(self, *args, **kwargs):
        # clean slate
        ReservationEquipment.objects.all().delete()
        Reservation.objects.all().delete()
        Equipment.objects.all().delete()
        Room.objects.all().delete()
        User.objects.all().delete()

        # ── SUPERUSER ──────────────────────────────────────────
        admin = User.objects.create_superuser(
            username="admin",
            password="admin",
            email="admin@skola.sk",
            first_name="Admin",
            last_name="System",
        )

        # ── USERS ──────────────────────────────────────────────
        users_data = [
            ("jnovak",    "Jan",     "Novak",    "jnovak@skola.sk"),
            ("mhorkova",  "Maria",   "Horkova",  "mhorkova@skola.sk"),
            ("pkubica",   "Peter",   "Kubica",   "pkubica@skola.sk"),
            ("zkovacova", "Zuzana",  "Kovacova", "zkovacova@skola.sk"),
            ("tbalog",    "Tomas",   "Balog",    "tbalog@skola.sk"),
            ("lkrupa",    "Lukas",   "Krupa",    "lkrupa@skola.sk"),
            ("evargova",  "Eva",     "Vargova",  "evargova@skola.sk"),
        ]
        users = {}
        for username, first, last, email in users_data:
            u = User.objects.create_user(
                username=username,
                password=username,
                email=email,
                first_name=first,
                last_name=last,
            )
            users[username] = u

        # ── ROOMS ──────────────────────────────────────────────
        rooms_data = [
            ("Ucebna A1",       101, 30, "UC", "Standardna ucebna s interaktivnou tabulou a projektorom."),
            ("Ucebna A2",       102, 25, "UC", "Standardna ucebna s projektorom."),
            ("Ucebna B1",       201, 28, "UC", "Ucebna s klimatizaciou a novymi lavicami."),
            ("Ucebna B2",       202, 28, "UC", "Ucebna vhodna pre skupinovu pracu."),
            ("Pocitacova sala", 301, 20, "LA", "Vybavena 20 PC stanicami a rychlym internetom."),
            ("Fyzikalne lab.",  302, 18, "LA", "Laboratorium pre fyzikalne experimenty."),
            ("Chemicke lab.",   303, 16, "LA", "Laboratorium s digestorom a bezpecnostnym vybavenim."),
            ("Biologicke lab.", 304, 16, "LA", "Laboratorium s mikroskopmi a preparatmi."),
            ("Telocvicna",      1,    0, "TE", "Velka telocvicna s parketovou podlahou."),
            ("Mala telocvicna", 2,    0, "TE", "Mala telocvicna pre mensi skupiny."),
            ("Kniznica",        401, 40, "KN", "Skolska kniznica s citarnou a studovnou."),
            ("Zborovna",        402, 20, "KA", "Zasadacia miestnost pre pedagogicky zbor."),
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

        # ── EQUIPMENT ──────────────────────────────────────────
        equipment_data = [
            ("Projektor Epson",     "EL", "Prenosny projektor 4000 lumenov s HDMI."),
            ("Projektor BenQ",      "EL", "Stropny projektor 3500 lumenov."),
            ("Notebook Dell",       "EL", "Ucitelsky notebook Dell Latitude s Windows 11."),
            ("Notebook Lenovo",     "EL", "Zalohy notebook Lenovo ThinkPad."),
            ("Interaktivna tabula", "EL", "Smart Board 75 palcov s dotykovym perom."),
            ("Mikrofon",            "EL", "Bezdrotovy mikrofon pre prezentacie."),
            ("Reproduktory",        "EL", "Prenosne Bluetooth reproduktory."),
            ("Stolicky skladacie",  "NA", "Skladacie stolicky pre extra kapacitu."),
            ("Stol skladaci",       "NA", "Lahky skladaci stol 180cm."),
            ("Tabule prenosna",     "NA", "Prenosna magneticka tabula na kolieskach."),
            ("Volejbalova siet",    "SP", "Suprava pre volejbal vratane stlpikov."),
            ("Basketbalove lopty",  "SP", "Sada 6 basketbalovych lopt Spalding."),
            ("Futbalove lopty",     "SP", "Sada 8 futbalovych lopt Nike."),
            ("Badminton suprava",   "SP", "4 rakety a 6 kosikov na badminton."),
        ]
        equipment = {}
        for nazov, typ, popis in equipment_data:
            e = Equipment.objects.create(
                nazovVybavenia=nazov,
                typVybavenia=typ,
                popis=popis,
            )
            equipment[nazov] = e

        # ── RESERVATIONS ───────────────────────────────────────
        # Spread across June 2026 including today (2026-06-03)
        reservations_data = [
            # June 2
            ("jnovak",    "Ucebna A1",       date(2026, 6, 2), time(8,  0), time(9,  30), "Matematika 3.A"),
            ("mhorkova",  "Ucebna A2",       date(2026, 6, 2), time(9,  0), time(10, 30), "Slovensky jazyk 2.B"),
            ("pkubica",   "Pocitacova sala", date(2026, 6, 2), time(10, 0), time(11, 30), "Informatika 4.A"),
            ("zkovacova", "Fyzikalne lab.",  date(2026, 6, 2), time(8,  0), time(10,  0), "Fyzika merania 3.B"),
            ("tbalog",    "Telocvicna",      date(2026, 6, 2), time(13, 0), time(15,  0), "Telesna vychova 1.A"),
            ("lkrupa",    "Biologicke lab.", date(2026, 6, 2), time(11, 0), time(13,  0), "Biologia pokusy 2.A"),
            ("evargova",  "Ucebna B1",       date(2026, 6, 2), time(9,  0), time(10, 30), "Dejepis 4.B"),

            # June 3 — today
            ("jnovak",    "Ucebna A1",       date(2026, 6, 3), time(8,  0), time(9,  30), "Matematika 4.B"),
            ("mhorkova",  "Ucebna A2",       date(2026, 6, 3), time(8,  0), time(9,  30), "Slovensky jazyk 3.A"),
            ("pkubica",   "Pocitacova sala", date(2026, 6, 3), time(9,  0), time(11,  0), "Programovanie 3.B"),
            ("zkovacova", "Chemicke lab.",   date(2026, 6, 3), time(10, 0), time(12,  0), "Chemia pokusy 2.A"),
            ("tbalog",    "Telocvicna",      date(2026, 6, 3), time(13, 0), time(15,  0), "Telesna vychova 2.B"),
            ("lkrupa",    "Ucebna B2",       date(2026, 6, 3), time(11, 0), time(12, 30), "Anglicky jazyk 1.A"),
            ("evargova",  "Kniznica",        date(2026, 6, 3), time(14, 0), time(16,  0), "Citatelsky kruzok"),
            ("admin",     "Zborovna",        date(2026, 6, 3), time(15, 0), time(16,  0), "Pedagogicka rada"),

            # June 4
            ("jnovak",    "Zborovna",        date(2026, 6, 4), time(14, 0), time(15,  0), "Porada kabinetu matematiky"),
            ("mhorkova",  "Ucebna A1",       date(2026, 6, 4), time(8,  0), time(9,  30), "Literatura 3.A"),
            ("pkubica",   "Pocitacova sala", date(2026, 6, 4), time(10, 0), time(12,  0), "Testovanie 4.A"),
            ("zkovacova", "Fyzikalne lab.",  date(2026, 6, 4), time(9,  0), time(11,  0), "Fyzika opakovanie 4.B"),
            ("tbalog",    "Mala telocvicna", date(2026, 6, 4), time(10, 0), time(11, 30), "Kruzok ping-pong"),
            ("lkrupa",    "Biologicke lab.", date(2026, 6, 4), time(8,  0), time(10,  0), "Biologia 3.A"),

            # June 5
            ("evargova",  "Ucebna B2",       date(2026, 6, 5), time(8,  0), time(9,  30), "Nemecky jazyk 2.B"),
            ("jnovak",    "Ucebna A2",       date(2026, 6, 5), time(10, 0), time(11, 30), "Matematika 1.B"),
            ("tbalog",    "Telocvicna",      date(2026, 6, 5), time(13, 0), time(15,  0), "Volejbalovy turnaj"),
            ("admin",     "Zborovna",        date(2026, 6, 5), time(16, 0), time(17,  0), "Stretnutie s rodicmi"),

            # June 8
            ("pkubica",   "Pocitacova sala", date(2026, 6, 8), time(8,  0), time(10,  0), "Informatika 3.A"),
            ("mhorkova",  "Kniznica",        date(2026, 6, 8), time(9,  0), time(11,  0), "Citatelsky projekt 4.A"),
            ("zkovacova", "Chemicke lab.",   date(2026, 6, 8), time(11, 0), time(13,  0), "Chemia opakovanie 3.B"),
            ("lkrupa",    "Ucebna B1",       date(2026, 6, 8), time(8,  0), time(9,  30), "Anglicky jazyk 2.A"),
            ("evargova",  "Ucebna A1",       date(2026, 6, 8), time(10, 0), time(11, 30), "Dejepis 3.B"),

            # June 9
            ("jnovak",    "Ucebna A1",       date(2026, 6, 9), time(8,  0), time(9,  30), "Matematika 2.A"),
            ("tbalog",    "Telocvicna",      date(2026, 6, 9), time(10, 0), time(12,  0), "Atletika 3.A"),
            ("pkubica",   "Pocitacova sala", date(2026, 6, 9), time(13, 0), time(15,  0), "Kruzok programovania"),

            # June 10
            ("admin",     "Zborovna",        date(2026, 6, 10), time(14, 0), time(16, 0), "Klasifikacna porada"),
            ("mhorkova",  "Ucebna B2",       date(2026, 6, 10), time(8,  0), time(9, 30), "Slovensky jazyk 4.A"),
            ("zkovacova", "Fyzikalne lab.",  date(2026, 6, 10), time(10, 0), time(12, 0), "Fyzika praktikum 3.A"),
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

        # ── EQUIPMENT ASSIGNMENTS ───────────────────────────────
        assignments = [
            ("pkubica",   "Informatika 4.A",          "Projektor Epson",    1, "Premietanie"),
            ("pkubica",   "Informatika 4.A",          "Notebook Dell",      1, ""),
            ("pkubica",   "Programovanie 3.B",        "Projektor BenQ",     1, ""),
            ("pkubica",   "Testovanie 4.A",           "Notebook Lenovo",    1, "Zaloha"),
            ("pkubica",   "Kruzok programovania",     "Projektor Epson",    1, ""),
            ("tbalog",    "Volejbalovy turnaj",        "Volejbalova siet",   1, ""),
            ("tbalog",    "Volejbalovy turnaj",        "Basketbalove lopty", 6, "Zalozne lopty"),
            ("tbalog",    "Telesna vychova 1.A",      "Futbalove lopty",    8, ""),
            ("tbalog",    "Atletika 3.A",             "Futbalove lopty",    4, ""),
            ("tbalog",    "Kruzok ping-pong",         "Badminton suprava",  2, "Ping-pong rakety"),
            ("admin",     "Pedagogicka rada",         "Projektor Epson",    1, ""),
            ("admin",     "Pedagogicka rada",         "Stolicky skladacie", 10, "Pre rodicov"),
            ("admin",     "Klasifikacna porada",      "Projektor BenQ",     1, ""),
            ("admin",     "Stretnutie s rodicmi",     "Stolicky skladacie", 20, ""),
            ("admin",     "Stretnutie s rodicmi",     "Mikrofon",           1, ""),
            ("jnovak",    "Porada kabinetu matematiky", "Interaktivna tabula", 1, ""),
            ("jnovak",    "Porada kabinetu matematiky", "Tabule prenosna",   1, ""),
            ("mhorkova",  "Citatelsky kruzok",        "Reproduktory",       1, "Hudba na pozadi"),
            ("evargova",  "Citatelsky kruzok",        "Reproduktory",       1, ""),
            ("zkovacova", "Fyzika merania 3.B",       "Notebook Dell",      1, "Zapis dat"),
        ]

        for username, ucel, vybavenie_nazov, pocet, poznamka in assignments:
            key = (username, ucel)
            if key in rezervacie:
                ReservationEquipment.objects.create(
                    rezervacia=rezervacie[key],
                    vybavenie=equipment[vybavenie_nazov],
                    pocetKusov=pocet,
                    poznamka=poznamka,
                )

        self.stdout.write(self.style.SUCCESS("Database populated successfully."))
        self.stdout.write(f"  Users:        {User.objects.count()}")
        self.stdout.write(f"  Rooms:        {Room.objects.count()}")
        self.stdout.write(f"  Equipment:    {Equipment.objects.count()}")
        self.stdout.write(f"  Reservations: {Reservation.objects.count()}")
        self.stdout.write("")
        self.stdout.write("Logins:")
        self.stdout.write("  admin        / admin")
        for username, *_ in users_data:
            self.stdout.write(f"  {username:<14} / {username}")