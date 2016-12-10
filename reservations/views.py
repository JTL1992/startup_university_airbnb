from datetime import datetime

import geocoder
from ajax_redirect import ajax_redirect
from django.contrib import messages
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext

from base.helper import convert_message_to_toastr
from reservations.models import Reservation
from rooms.models import Room, Location, Calender


def reservation_date(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.is_ajax():
        if request.method == 'GET':
            date_range_invalid = []
            min_date = room.calender.date_range.split(' - ')[0]
            max_date = room.calender.date_range.split(' - ')[1]
            try:
                reservations = room.reservation_set.all()
                for reservation in reservations:
                    date_range_invalid.append(reservation.date_range)
            except Reservation.DoesNotExist:
                date_range_invalid = []
            reservation = {
                'min_date': min_date,
                'max_date': max_date,
                'date_range_invalid': date_range_invalid,
                'price': room.price.price
            }
            return JsonResponse(reservation)
        if request.method == 'POST':
            total = request.POST['total']
            date_range = request.POST['date_range']
            reservation = Reservation(room=room, guest=request.user, total=total, date_range=date_range, price=room.price.price)
            reservation.save()
            messages.add_message(request, messages.SUCCESS, 'Book successfully!')
            print('success')
            return JsonResponse({'ok': 200})


def reservation_list(request):
    rooms = request.user.room_set.all()
    reservations = []
    for room in rooms:
        reservations += room.reservation_set.all()
    return render_to_response('room_list.html', {'reservations': reservations,
                                                 'render_view': 'reservation_list_view.html'}, RequestContext(request))


def trip_list(request):
    message = convert_message_to_toastr(messages.get_messages(request))
    reservations = request.user.reservation_set.all()
    return render_to_response('room_list.html', {'trips': reservations,
                                                 'render_view': 'trip_list_view.html', 'messages': message}, RequestContext(request))


@ajax_redirect
def search(request):
    if request.method == 'GET':
        place = request.GET.get('place')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date != '':
            start_date = datetime.strptime(start_date, '%m/%d/%Y')
            end_date = datetime.strptime(end_date, '%m/%d/%Y')
        else:
            start_date = datetime.today()
            end_date = datetime.today()
        print(start_date)
        guests = request.GET.get('guest') or 1
        print(guests)
        g = geocoder.google(place)
        print(g.json)
        if g.ok:
            if g.postal:
                locations = Location.objects.filter(administrative_area_level_1=g.state, locality=g.city, postal_code=g.postal)
                if not locations:
                    locations = Location.objects.filter(administrative_area_level_1=g.state, locality=g.city)
            else:
                locations = Location.objects.filter(administrative_area_level_1=g.state, locality=g.city)
        else:
            print('address input wrong')
            return render_to_response('home.html', RequestContext(request))
        print(locations)
        calendars = Calender.objects.filter(start_date__lte=start_date, end_date__gte=end_date)
        print(calendars)
        rooms = Room.objects.filter(is_active=True, accommodate__gte=guests, calender__in=calendars, location__in=locations)
        located_rooms = Location.objects.filter(room__in=rooms)
        rooms_location = serializers.serialize('json', located_rooms)
        return render_to_response('room_search.html', {'rooms': rooms, 'rooms_data': rooms_location}, RequestContext(request))



