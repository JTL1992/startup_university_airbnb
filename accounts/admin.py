from django.contrib import admin
from accounts import models
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_avatar', 'user', 'phone', 'description')
    search_fields = ('user__username',)
    readonly_fields = ('user_avatar', 'image_url')

admin.site.register(models.UserProfile, UserProfileAdmin)
