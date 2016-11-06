from django.conf.urls import include, url


# this is a url dispatcher for room creating


urlpatterns = [
    url(r'^$', 'rooms.views.become_a_host', name='become_a_host'),
    url(r'^rooms$', 'rooms.views.room_list', name='rooms_list'),
    url(r'^(?P<room_id>\d+)/section/$', 'rooms.views.room_section', name='room_section'),
    url(r'^(?P<room_id>\d+)/home_type/$', 'rooms.views.home_type_view', name='home_type'),
    url(r'^(?P<room_id>\d+)/bedrooms/$', 'rooms.views.bedrooms', name='bedrooms'),
    url(r'^(?P<room_id>\d+)/bathrooms/$', 'rooms.views.bathrooms', name='bathrooms'),
    url(r'^(?P<room_id>\d+)/location/$', 'rooms.views.location', name='location'),
    url(r'^(?P<room_id>\d+)/location/map/$', 'rooms.views.location_map'),
    url(r'^(?P<room_id>\d+)/amenities/$', 'rooms.views.amenities', name='amenities'),
    url(r'^(?P<room_id>\d+)/spaces/$', 'rooms.views.spaces', name='spaces'),
    url(r'^(?P<room_id>\d+)/photos/$', 'rooms.views.photos', name='photos'),
    url(r'^(?P<room_id>\d+)/highlights/$', 'rooms.views.highlights', name='highlights'),
    url(r'^(?P<room_id>\d+)/name_description/$', 'rooms.views.name_description', name='name_description'),
    url(r'^(?P<room_id>\d+)/calenders/$', 'rooms.views.calenders', name='calenders'),
    url(r'^(?P<room_id>\d+)/price/$', 'rooms.views.price', name='price'),
    url(r'^(?P<room_id>\d+)/$', 'rooms.views.rooms', name='room_view'),
    url(r'^(?P<room_id>\d+)/active/$', 'rooms.views.active'),







]
