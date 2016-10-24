from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    phone = models.CharField(max_length=20)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.phone
