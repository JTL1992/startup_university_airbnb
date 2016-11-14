from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'reservations.views.reservation_list', name='reservation_list'),
]