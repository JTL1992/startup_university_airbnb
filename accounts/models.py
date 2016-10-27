from django.db import models
from django.contrib.auth.models import User
from base.helper import get_user_avatar
import hashlib
import urllib
from django import template
from django.utils.safestring import mark_safe
# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, verbose_name='username')
    phone = models.IntegerField(verbose_name='phone number')
    description = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200, default='https://example.com/static/images/defaultavatar.jpg')

    def __unicode__(self):
        return self.user.username

    def user_avatar(self):
            return u'<img width="100" height="100" src="%s"/>' % self.image_url
    user_avatar.short_description = 'Image'
    user_avatar.allow_tags = True



