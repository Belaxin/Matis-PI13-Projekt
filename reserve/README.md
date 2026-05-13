# Rezervačný systém učební

Webová aplikácia na rezerváciu učební, laboratórií a iných školských miestností. Vytvorená ako školský projekt v rámci predmetu Programovanie.

## Funkcie

- Prezeranie a rezervovanie miestností
- Kontrola kolízií termínov (systém nedovolí dve rezervácie v rovnakom čase)
- Priradenie vybavenia k rezervácii
- Filtrovanie rezervácií podľa dátumu, miestnosti a účelu
- Dve používateľské roly — bežný používateľ a administrátor
- REST API endpointy pre miestnosti a rezervácie
- Administrátorský panel pre správu používateľov, miestností a vybavenia

## Technológie

| Vrstva | Technológia |
|--------|-------------|
| Backend | Django 5.0 |
| Databáza | PostgreSQL (produkcia) / SQLite (vývoj) |
| Frontend | Django Templates + Bootstrap 5 |
| Hosting | Render |
| Statické súbory | WhiteNoise |

## Modely

- **Room** — miestnosť s názvom, číslom, kapacitou a typom
- **Equipment** — vybavenie s typom a popisom
- **Reservation** — rezervácia prepojená na miestnosť a používateľa
- **ReservationEquipment** — M:N vzťah medzi rezerváciou a vybavením (s počtom kusov)

## Inštalácia (lokálne)

```bash
git clone <url-repozitara>
cd reserve

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env          # uprav SECRET_KEY a ostatné hodnoty

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Aplikácia beží na http://127.0.0.1:8000

## Používateľské roly

| Rola | Možnosti |
|------|----------|
| Bežný používateľ | Vytvárať, upravovať a rušiť vlastné rezervácie, prezerať všetky rezervácie a miestnosti |
| Administrátor | Všetko vyššie + správa miestností, vybavenia a používateľov |

## REST API

| Endpoint | Popis |
|----------|-------|
| `GET /api/miestnosti/` | Zoznam všetkých miestností |
| `GET /api/miestnosti/<id>/` | Detail miestnosti s rezerváciami |
| `GET /api/rezervacie/` | Zoznam rezervácií |
| `GET /api/rezervacie/<id>/` | Detail rezervácie s vybavením |

Všetky endpointy vyžadujú prihlásenie a podporujú filtrovanie cez GET parametre.

## Autor

Školský projekt — 3. ročník, predmet Programovanie
