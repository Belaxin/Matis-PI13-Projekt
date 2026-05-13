# Technická dokumentácia

## Štruktúra projektu

```
reserve/                  ← projektový priečinok (settings, urls)
rezervacie/               ← hlavná aplikácia
  models.py               ← databázové modely
  views.py                ← logika stránok
  api.py                  ← REST API endpointy
  forms.py                ← Django formuláre
  urls.py                 ← URL smery
  admin.py                ← registrácia modelov v admin paneli
  templates/
    rezervacie/
      base.html           ← základný layout (navbar, Bootstrap)
      index.html          ← dashboard
      reservation_*.html  ← šablóny pre rezervácie
      room_*.html         ← šablóny pre miestnosti
      equipment_*.html    ← šablóny pre vybavenie
      admin_*.html        ← šablóny pre admin panel
```

## Databázové modely

### Room
| Pole | Typ | Popis |
|------|-----|-------|
| nazovMiestnosti | CharField | Názov miestnosti |
| cisloMiestnosti | IntegerField | Číslo miestnosti |
| kapacitaMiestnosti | IntegerField | Maximálny počet osôb |
| typMiestnosti | CharField (choices) | Učebňa / Laboratórium / Telocvičňa / ... |
| popisMiestnosti | CharField | Voliteľný popis |

### Reservation
| Pole | Typ | Popis |
|------|-----|-------|
| datumRezervacie | DateField | Dátum |
| casOd | TimeField | Čas začiatku |
| casDo | TimeField | Čas konca |
| ucelRezervacie | CharField | Účel rezervácie |
| miestnostRezervacie | ForeignKey → Room | Miestnosť |
| pouzivatelRezervacie | ForeignKey → User | Používateľ |
| vybavenie | ManyToManyField → Equipment (through ReservationEquipment) | Priradené vybavenie |

### Equipment
| Pole | Typ | Popis |
|------|-----|-------|
| nazovVybavenia | CharField | Názov |
| typVybavenia | CharField (choices) | Elektronika / Nábytok / Šport / Iné |
| popis | CharField | Voliteľný popis |

### ReservationEquipment (M:N through model)
| Pole | Typ | Popis |
|------|-----|-------|
| rezervacia | ForeignKey → Reservation | |
| vybavenie | ForeignKey → Equipment | |
| pocetKusov | IntegerField | Počet kusov |
| poznamka | CharField | Voliteľná poznámka |

## Kontrola kolízií

Logika je implementovaná v `Reservation.clean()` v `models.py`.

Dve časové okná `[A, B]` a `[C, D]` sa prekrývajú keď: `A < D AND C < B`.

V Django ORM:
```python
Reservation.objects.filter(
    miestnostRezervacie=self.miestnostRezervacie,
    datumRezervacie=self.datumRezervacie,
    casOd__lt=self.casDo,
    casDo__gt=self.casOd,
).exclude(pk=self.pk)
```

`exclude(pk=self.pk)` zabezpečuje, že pri úprave rezervácia nekoliduje sama so sebou.

## Používateľské roly

Implementované cez Django zabudovaný `User` model:
- `is_staff = False` → bežný používateľ
- `is_staff = True` → administrátor

Ochrana views pomocou dekorátorov:
```python
@login_required                  # musí byť prihlásený
@user_passes_test(is_admin)      # musí byť admin
```

## Nasadenie

Aplikácia je nasadená na platforme Render.

- **Web service** — Gunicorn WSGI server
- **Databáza** — PostgreSQL (Render managed)
- **Statické súbory** — WhiteNoise middleware
- **Environment variables** — SECRET_KEY, DEBUG, ALLOWED_HOSTS, DATABASE_URL
