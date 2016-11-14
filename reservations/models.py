from django.contrib.auth.models import User
from django.db import models
from django import forms
# Create your models here.
from rooms.models import Room


class Reservation(models.Model):
    room = models.ForeignKey(Room)
    guest = models.ForeignKey(User)
    date_range = models.CharField(max_length=30, verbose_name='Book in and out')
    total = models.CharField(max_length=10)
    price = models.CharField(max_length=10)
    created_at = models.DateField(auto_created=True, auto_now=True)

    def __unicode__(self):
        return self.guest.username


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date_range', 'total', 'price']
        widgets = {
            'total': forms.TextInput(attrs={'readonly': True, 'class': 'total-input'})
        }