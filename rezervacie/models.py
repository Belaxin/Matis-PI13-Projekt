from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    class Typ(models.TextChoices):
        UCEBNA      = "UC", "Učebňa"
        LABORATORIUM = "LA", "Laboratórium"
        TELOCVICNA  = "TE", "Telocvičňa"
        KANCELARIA  = "KA", "Kancelária"
        KNIZNICA    = "KN", "Knižnica"
        INE         = "IN", "Iné"
    
    nazovMiestnosti = models.CharField(max_length=100)
    cisloMiestnosti = models.IntegerField()
    kapacitaMiestnosti = models.IntegerField()
    typMiestnosti = models.CharField(max_length=2, choices=Typ.choices, default=Typ.INE)
    popisMiestnosti = models.CharField(max_length=500, null=True, blank=True)
    def __str__(self):
        return self.nazovMiestnosti

class Equipment(models.Model):
    class Typ(models.TextChoices):
        ELEKTRONIKA = "EL", "Elektronika"
        NABYTOK     = "NA", "Nábytok"
        SPORT       = "SP", "Šport"
        INE         = "IN", "Iné"
    nazovVybavenia = models.CharField(max_length=100)
    popis = models.CharField(max_length=500, null=True, blank=True)
    typVybavenia = models.CharField(max_length=2, choices=Typ.choices, default=Typ.INE)
    def __str__(self):
        return self.nazovVybavenia



class Reservation(models.Model):
    datumRezervacie = models.DateField(auto_now=False, auto_now_add=False)
    casOd = models.TimeField(auto_now=False, auto_now_add=False)
    casDo = models.TimeField(auto_now=False, auto_now_add=False)
    ucelRezervacie = models.CharField(max_length=100)
    vybavenie = models.ManyToManyField(Equipment, through="ReservationEquipment", null=True, blank=True)
    miestnostRezervacie = models.ForeignKey(          
        Room,
        on_delete=models.CASCADE,
        related_name="rezervacie",
        null=True,                       
        blank=True,
    )
    pouzivatelRezervacie = models.ForeignKey(          
        User,
        on_delete=models.CASCADE,
        related_name="rezervacie",
        null=True,                       
        blank=True,
    )
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(casDo__gt=models.F("casOd")),
                name="casDo_must_be_after_casOd"
            )
        ]

    @property
    def nazovRezervacie(self):
        pouzivatel = self.pouzivatelRezervacie.username + self.pouzivatelRezervacie.Priezvisko if self.pouzivatelRezervacie else "Anonym"
        miestnost = self.miestnostRezervacie.nazovMiestnosti if self.miestnostRezervacie else "Neznáma"
        
        return f"{pouzivatel} - {miestnost} ({self.datumRezervacie})"

    def __str__(self):
        return self.nazovRezervacie



class ReservationEquipment(models.Model):
    rezervacia = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    vybavenie  = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    pocetKusov = models.IntegerField()
    poznamka = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"{self.rezervacia} - {self.vybavenie} x{self.pocetKusov}"
