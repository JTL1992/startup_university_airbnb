from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext

from base.helper import convert_message_to_toastr
from reservations.models import Reservation
from rooms.models import Room


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

