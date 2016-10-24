from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'base.views.home', name='home'),
    url(r'^accounts/profile/$', 'accounts.views.my_profile', name='account_profile'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),

]
