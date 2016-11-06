from django.contrib import admin

# Register your models here.
from rooms.models import Room, Location, HomeType, Bedroom, Bathroom, Amenity, SpaceShare, Photo, HighLight,\
    NameDescription, Calender, Price


class RoomsAdmin(admin.ModelAdmin):
    list_display = ('owner', 'room_type', 'accommodate', 'create_date')
    search_fields = ('owner__username',)
    readonly_fields = ('owner', 'create_date')
    ordering = ('-create_date',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('room', 'formatted_address')
    search_fields = ('owner__username',)
    ordering = ('-room__create_date',)


class HomeTypeAdmin(admin.ModelAdmin):
    list_display = ('room', 'home_type', 'room_type')
    search_fields = ('owner__username',)
    ordering = ('-room__create_date',)


class BedroomAdmin(admin.ModelAdmin):
    list_display = ('room', 'bed_type', 'num_bed', 'num_guest')
    search_fields = ('owner__username',)
    ordering = ('-room__create_date',)


class BathroomAdmin(admin.ModelAdmin):
    list_display = ('room', 'num_bathroom')
    search_fields = ('owner__username',)
    ordering = ('-room__create_date',)


class AmenityAdmin(admin.ModelAdmin):
    list_display = ('room',)
    search_fields = ('owner__username',)
    ordering = ('-room__create_date',)


class SpaceAdmin(admin.ModelAdmin):
    list_display = ('room',)
    search_fields = ('owner__username',)
    ordering = ('-room__create_date',)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('room',)
    search_fields = ('owner__username',)
    ordering = ('-room__create_date',)


class HighLightAdmin(admin.ModelAdmin):
    list_display = ('room', 'close_to', 'love_for')
    search_fields = ('owner__username',)
    ordering = ('-room__create_date',)


class NameDescriptionAdmin(admin.ModelAdmin):
    list_display = ('room', 'room_name', 'room_description')
    search_fields = ('owner__username',)
    ordering = ('-room__create_date',)


class CalenderAdmin(admin.ModelAdmin):
    list_display = ('room', 'date_range')
    search_fields = ('owner__username',)
    ordering = ('-room__create_date',)


class PriceAdmin(admin.ModelAdmin):
    list_display = ('room', 'price')
    search_fields = ('owner__username',)
    ordering = ('-room__create_date',)

admin.site.register(Room, RoomsAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(HomeType, HomeTypeAdmin)
admin.site.register(Bedroom, BedroomAdmin)
admin.site.register(Bathroom, BathroomAdmin)
admin.site.register(Amenity, AmenityAdmin)
admin.site.register(SpaceShare, SpaceAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(HighLight, HighLightAdmin)
admin.site.register(NameDescription, NameDescriptionAdmin)
admin.site.register(Calender, CalenderAdmin)
admin.site.register(Price, PriceAdmin)

