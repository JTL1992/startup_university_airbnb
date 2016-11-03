from django.contrib import admin

# Register your models here.
from rooms.models import Room, Location


class RoomsAdmin(admin.ModelAdmin):
    list_display = ('owner', 'room_type', 'accommodate', 'create_date')
    search_fields = ('owner__username',)
    readonly_fields = ('owner', 'create_date')
    ordering = ('-create_date',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('room', 'formatted_address')
    search_fields = ('owner__username',)
    ordering = ('-room__create_date',)
admin.site.register(Room, RoomsAdmin)
admin.site.register(Location, LocationAdmin)

