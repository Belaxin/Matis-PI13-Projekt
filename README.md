# Matis-PI13-Projekt
Zadanie 3: Webová aplikácia „Rezervačný systém učební“

Cieľ projektu

Vytvorte webovú aplikáciu na rezerváciu učební, laboratórií alebo iných školských miestností.

Backend musí byť vytvorený v Django.
Frontend je ľubovoľný.

Aplikácia musí byť na konci projektu nasadená online na free platforme.

Opis aplikácie

Škola potrebuje systém, v ktorom bude možné:

- evidovať miestnosti
- evidovať rezervácie
- prideľovať vybavenie k rezervácii
- kontrolovať kolízie termínov
- zobrazovať prehľad rezervácií podľa dátumu a miestnosti

Povinné modely

1. Room
- názov miestnosti
- číslo miestnosti
- kapacita
- typ miestnosti
- popis

2. Reservation
- názov rezervácie
- dátum
- čas od
- čas do
- účel rezervácie
- miestnosť
- používateľ

3. Equipment
- názov vybavenia
- typ
- počet kusov
- popis

4. User
- používateľ rezervácie

Povinný M:N vzťah

Povinné riešenie:
Reservation ↔ Equipment

Odporúčané riešenie cez model ReservationEquipment
- rezervácia
- vybavenie
- počet kusov
- poznámka

Povinné funkcionality

CRUD operácie

Minimálne pre:
- Room
- Reservation
- Equipment

Rezervácie
- vytvoriť rezerváciu
- zrušiť rezerváciu
- kontrolovať kolízie termínov
- priradiť vybavenie k rezervácii
- zobraziť rezervácie konkrétnej miestnosti

Vyhľadávanie a filtrovanie
- podľa dátumu
- podľa miestnosti
- podľa používateľa
- podľa typu miestnosti

Prihlásenie používateľa

Minimálne 2 roly:
- administrátor
- bežný používateľ

API alebo frontend
- Django templates + jednoduché API
alebo
- oddelený frontend + REST API

Povinné nasadenie

Projekt musí byť nasadený online na free platforme.

Povinné odovzdanie
- Git repozitár
- odkaz na aplikáciu
- README
- stručná dokumentácia
- prezentácia

Spoločné požiadavky pre všetky zadania

Každý projekt musí obsahovať:
- backend v Django
- databázové modely a migrácie
- aspoň jeden vzťah M:N
- CRUD operácie nad hlavnými entitami
- autentifikáciu používateľa
- minimálne 2 používateľské roly
- filtrovanie alebo vyhľadávanie
- Git repozitár
- README
- nasadenie na free platforme
