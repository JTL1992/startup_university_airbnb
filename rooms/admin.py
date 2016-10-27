from django.contrib import admin

# Register your models here.
from rooms.models import Room


class RoomsAdmin(admin.ModelAdmin):
    list_display = ('owner', 'room_type', 'accommodate', 'create_date')
    search_fields = ('owner__username',)
    readonly_fields = ('owner', 'create_date')
    ordering = ('-create_date',)
admin.site.register(Room, RoomsAdmin)
