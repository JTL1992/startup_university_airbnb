from django.db import models
from django import forms
# Create your models here.


class Location(models.Model):
    format_address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state_province = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip = models.CharField(max_length=20)
    lat = models.CharField(max_length=50)
    lng = models.CharField(max_length=50)

    def __unicode__(self):
        return self.format_address


class LocationsForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
        exclude = ['lat', 'lng']
        widgets = {
            # 'title': forms.TextInput(attrs={'placeholder': 'A good name for your house'}),
            # 'description': forms.Textarea(attrs={'cols': 80, 'rows': 5, 'placeholder': 'Tell us about your house'}),
            # 'price': forms.TextInput(attrs={'placeholder': 'for example: 30'})
        }
