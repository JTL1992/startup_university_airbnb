# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django import forms

ROOM_TYPE_CHOICES = (
    ('Entire place', 'Entire place'),
    ('Private room', 'Private room'),
    ('Share room', 'Share room'),
)
ACCOMMODATE_CHOICES = (
    (s, s) for s in range(1, 6)
)
BEDROOM_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
)
HOME_TYPE_CHOICES = (
    ('Apartment', 'Apartment'),
    ('House', 'House'),
    ('Bed & Breakfast', 'Bed & Breakfast'),
    ('Other', 'Other'),
)
BED_CHOICES = (
    ('real bed', 'real bed'),
    ('pull-out sofa', 'pull-out sofa'),
    ('airbed', 'airbed'),
    ('futon', 'futon'),
    ('couch', 'couch'),
)


class Room(models.Model):
    room_type = models.CharField(max_length=100, choices=ROOM_TYPE_CHOICES, default='Entire place')
    accommodate = models.IntegerField(choices=ACCOMMODATE_CHOICES, verbose_name='Accommodates',
                                      default='1')
    is_active = models.BooleanField()
    create_date = models.DateTimeField(auto_now_add=True)
    city_country = models.CharField(max_length=50, verbose_name='City, Country', blank=False, default='')
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.owner.username


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['owner', 'is_active', 'created_date']


class HomeType(models.Model):
    room = models.OneToOneField(Room)
    room_type = models.CharField(max_length=20, default='Entire place')
    home_type = models.CharField(max_length=20, choices=HOME_TYPE_CHOICES, default='Apartment')

    def __unicode__(self):
        return self.room.owner.username


class HomeTypeForm(forms.ModelForm):
    class Meta:
        model = HomeType
        Fields = '_all_'
        exclude = ['room']
        widgets = {
            'room_type': forms.RadioSelect(choices=ROOM_TYPE_CHOICES)
        }


class Bedroom(models.Model):
    room = models.OneToOneField(Room)
    num_bed = models.IntegerField(verbose_name='how many beds?', default=1)
    num_guest = models.IntegerField(verbose_name='', default=1)
    bed_type = models.CharField(max_length=15)

    def __unicode__(self):
        return self.room.owner.username


class BedroomForm(forms.ModelForm):
    class Meta:
        model = Bedroom
        Fields = '_all_'
        exclude = ['room']
        widgets = {
            'bed_type': forms.Select(choices=BED_CHOICES)
        }


class Bathroom(models.Model):
    room = models.OneToOneField(Room)
    num_bathroom = models.IntegerField(verbose_name="", default=1)

    def __unicode__(self):
        return self.room.owner.username


class BathroomForm(forms.ModelForm):
    class Meta:
        model = Bathroom
        Fields = '_all_'
        exclude = ['room']


class Location(models.Model):
    room = models.OneToOneField(Room)
    formatted_address = models.CharField(max_length=100, verbose_name='Full Address')
    country = models.CharField(max_length=50, verbose_name='Country')
    route = models.CharField(max_length=50, verbose_name='Street Address')
    street_number = models.CharField(max_length=10, verbose_name='Street Number')
    locality = models.CharField(max_length=50, verbose_name='City')
    postal_code = models.CharField(max_length=10, verbose_name='ZIP Code')
    administrative_area_level_1 = models.CharField(max_length=50, verbose_name='State')
    lat = models.CharField(max_length=50)
    lng = models.CharField(max_length=50)

    def __unicode__(self):
        return self.room.owner.username


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        Fields = '_all_'
        exclude = ['room', 'formatted_address', 'lat', 'lng']


class Amenity(models.Model):
    room = models.OneToOneField(Room)
    is_essential = models.BooleanField(verbose_name='Essentials')
    is_wifi = models.BooleanField(verbose_name='Wifi')
    is_drawer = models.BooleanField(verbose_name='Closet/drawers')
    is_tv = models.BooleanField(verbose_name='TV')
    is_heat = models.BooleanField(verbose_name='Heat')
    is_air = models.BooleanField(verbose_name='Air conditioning')
    is_breakfast = models.BooleanField(verbose_name='Breakfast, coffee, tea')
    is_desk = models.BooleanField(verbose_name='Desk/workspace')
    is_fireplace = models.BooleanField(verbose_name='Fireplace')
    is_iron = models.BooleanField(verbose_name='Iron')
    is_hairdryer = models.BooleanField(verbose_name='Hair dryer')

    def __unicode__(self):
        return self.room.owner.username


class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        Fields = '_all_'
        exclude = ['room']


class SpaceShare(models.Model):
    room = models.OneToOneField(Room)
    is_kitchen = models.BooleanField(verbose_name='Kitchen')
    is_laundry_washer = models.BooleanField(verbose_name='Laundry-washer')
    is_laundry_dryer = models.BooleanField(verbose_name='Laundry-dryer')
    is_parking = models.BooleanField(verbose_name='Parking')
    is_elevator = models.BooleanField(verbose_name='Elevator')
    is_pool = models.BooleanField(verbose_name='Pool')
    is_hot_tub = models.BooleanField(verbose_name='Hot tub')
    is_gym = models.BooleanField(verbose_name='Gym')

    def __unicode__(self):
        return self.room.owner.username


class SpaceShareForm(forms.ModelForm):
    class Meta:
        model = SpaceShare
        Fields = '_all_'
        exclude = ['room']
