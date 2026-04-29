from django.contrib import admin
from .models import Room, Reservation, Equipment, ReservationEquipment

admin.site.register(Room)
admin.site.register(Equipment)


class EquipmentInline(admin.TabularInline):
    model = ReservationEquipment
    extra = 1


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    inlines = [EquipmentInline]
    exclude = ('vybavenie',)