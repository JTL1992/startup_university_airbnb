from django.contrib import admin

# Register your models here.
from reservations.models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('room', 'guest', 'date_range', 'price', 'total')
    search_fields = ('room.owner__username', 'guest__username')
    ordering = ('-created_at',)


admin.site.register(Reservation, ReservationAdmin)
