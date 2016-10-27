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


class Location(models.Model):
    room = models.OneToOneField(Room)
    address = models.CharField(max_length=200)
    lat = models.FloatField()
    lng = models.FloatField()
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    zip = models.IntegerField()

    def __unicode__(self):
        return self.room.owner.username


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        Fields = '_all_'
        exclude = ['room']


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
