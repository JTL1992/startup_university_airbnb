from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'base.views.home', name='home'),
    url(r'^accounts/profile/$', 'accounts.views.my_profile', name='account_profile'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^users/(?P<user_id>\d+)/$', 'accounts.views.public_profile', name='public_profile'),
    url(r'rooms/', include('rooms.urls')),
    url(r'^reservations/$', 'reservations.views.reservation_list', name='reservation_list'),
    url(r'^trips/$', 'reservations.views.trip_list', name='trip_list')


]
