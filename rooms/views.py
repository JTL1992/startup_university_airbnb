from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response


# Create your views here.
from django.template import RequestContext

from rooms.models import RoomForm, HomeTypeForm, Room


@login_required()
def become_a_host(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.owner = request.user
            room.is_active = False
            room.save()
            messages.add_message(request, messages.SUCCESS, 'Create your room successfully!')
            return HttpResponseRedirect(reverse('home_type', kwargs={'room_id': room.id}))
    else:
        form = RoomForm()
    return render_to_response('room_create.html', {'form': form}, RequestContext(request))


def room_list(request):
    user = request.user
    if user.room_set.all().count():
        user_rooms = user.room_set.all()
    else:
        user_rooms = None
    return render_to_response('room_list.html', {'rooms': user_rooms}, RequestContext(request))


def room_section(request, room_id):
    return render_to_response('room_section.html', RequestContext(request))


def home_type_view(request, room_id):
    if request.method == 'POST':
        form = HomeTypeForm(request.POST)
        if form.is_valid():
            home_type = form.save(commit=False)
            home_type.room = Room.objects.get(id=room_id)
            home_type.save()
            messages.add_message(request, messages.SUCCESS, 'edit your room type successfully!')
            return HttpResponseRedirect(reverse('home_type', kwargs={'room_id': room_id}))
    else:
        room = Room.objects.get(id=room_id)
        if hasattr(room, 'hometype'):
            home_type = room.hometype
            form = HomeTypeForm(instance=home_type)
        else:
            form = HomeTypeForm()
    return render_to_response('home_type.html', {'form': form, 'room_id': room_id}, RequestContext(request))

