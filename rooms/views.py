import json

import geocoder
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render_to_response
from django.forms.models import model_to_dict


# Create your views here.
from django.template import RequestContext

from base.helper import convert_message_to_toastr
from reservations.models import Reservation, ReservationForm
from rooms.models import Location, Amenity, AmenityForm, SpaceShare, SpaceShareForm, Photo, PhotoForm, HighLight, \
    HighLightForm, NameDescription, NameDescriptionForm, Calender, CalenderForm, Price, PriceForm
from rooms.models import RoomForm, HomeTypeForm, Room, BedroomForm, HomeType, Bedroom, BathroomForm, Bathroom, \
    LocationForm


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


@login_required()
def room_list(request):
    message = convert_message_to_toastr(messages.get_messages(request))
    user = request.user
    if user.room_set.all().count():
        user_rooms = user.room_set.all()
    else:
        user_rooms = None
    return render_to_response('room_list.html', {'rooms': user_rooms, 'messages': message, 'render_view': 'room_list_view.html'}, RequestContext(request))


@login_required()
def room_section(request, room_id):
    model_list = ('hometype', 'bedroom', 'bathroom', 'location', 'amenity', 'spaceshare',
                  'photo', 'highlight', 'namedescription', 'calender', 'price')
    page_list = ('home_type', 'bedrooms', 'bathrooms', 'location', 'amenities', 'spaces',
                 'photos', 'highlights', 'name_description', 'calenders', 'price')
    room = Room.objects.get(id=room_id)
    page_url = ['home_type', 'photos', 'calenders']
    button = ['Change', None, None, None]
    for index, section in enumerate(model_list):
        if not hasattr(room, section):
            if index < 5:
                button[0] = 'Continue'
                page_url[0] = page_list[index]
            elif 5 <= index < 8:
                button[1] = 'Continue'
                page_url[1] = page_list[index]
            else:
                button[1] = 'Change'
                button[2] = 'Continue'
                page_url[2] = page_list[index]
            break
        else:
            if index == 10:
                button = ['Change', 'Change', 'Change', None]
                if room.is_active:
                    button[3] = 'Deactive'
                else:
                    button[3] = 'Active'

    return render_to_response('room_section.html', {'page_url': page_url, 'button': button, 'room_id': room_id}, RequestContext(request))


def home_type_view(request, room_id):
    room = Room.objects.get(id=room_id)
    message = convert_message_to_toastr(messages.get_messages(request))
    try:
        home_type = room.hometype
    except HomeType.DoesNotExist:
        home_type = HomeType(room=room)
    if request.method == 'POST':
        form = HomeTypeForm(request.POST,instance=home_type)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'edit your room type successfully!')
            return HttpResponseRedirect(reverse('bedrooms', kwargs={'room_id': room_id},))
    else:
        form = HomeTypeForm(instance=home_type)
    return render_to_response('home_type.html', {'form': form, 'room_id': room_id, 'messages': message}, RequestContext(request))


def bedrooms(request, room_id):
    room = Room.objects.get(id=room_id)
    message = convert_message_to_toastr(messages.get_messages(request))
    try:
        bedroom = room.bedroom
    except Bedroom.DoesNotExist:
        bedroom = Bedroom(room=room)
    if request.method == 'POST':
        form = BedroomForm(request.POST, instance=bedroom)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'edit your bedroom successfully!')
            return HttpResponseRedirect(reverse('bathrooms', kwargs={'room_id': room_id}))
    else:
        form = BedroomForm(instance=bedroom)
    return render_to_response('bedroom.html', {'form': form, 'room_id': room_id, 'messages': message}, RequestContext(request))


def bathrooms(request, room_id):
    room = Room.objects.get(id=room_id)
    message = convert_message_to_toastr(messages.get_messages(request))
    try:
        bathroom = room.bathroom
    except Bathroom.DoesNotExist:
        bathroom = Bathroom(room=room)
    if request.method == 'POST':
        form = BathroomForm(request.POST, instance=bathroom)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'edit your bathroom successfully!')
            return HttpResponseRedirect(reverse('location', kwargs={'room_id': room_id}))
    else:
        form = BathroomForm(instance=bathroom)
    return render_to_response('bathroom.html', {'form': form, 'room_id': room_id, 'messages': message}, RequestContext(request))


def location(request, room_id):
    message = convert_message_to_toastr(messages.get_messages(request))
    room = Room.objects.get(id=room_id)
    g = geocoder.google(room.city_country)
    try:
        address = room.location
    except Location.DoesNotExist:
        address = Location(room=room, country=room.city_country.split(', ')[1],
                           locality=room.city_country.split(', ')[0], administrative_area_level_1=g.state)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=address)
        if form.is_valid():
            route = form.cleaned_data['route']
            street_number = form.cleaned_data['street_number']
            locality = form.cleaned_data['locality']
            country = form.cleaned_data['country']
            postal_code = form.cleaned_data['postal_code']

            input_address = '%s %s, %s, %s' % (route, street_number, locality, country)
            g = geocoder.google(input_address)
            if g.ok and g.postal == postal_code:
                data = form.save()
                data.formatted_address = g.address
                data.lat = g.lat
                data.lng = g.lng
                data.save()
                messages.add_message(request, messages.SUCCESS, 'edit your location successfully!')
                message = convert_message_to_toastr(messages.get_messages(request))
                return render_to_response('location_map.html', {'messages': message, 'room_id': room_id}, RequestContext(request))
            else:
                messages.add_message(request, messages.ERROR, 'Something wrong with your location!')
                message = convert_message_to_toastr(messages.get_messages(request))
                render_to_response('location.html', {'form': form, 'room_id': room_id, 'messages': message},
                                   RequestContext(request))
    else:
        form = LocationForm(instance=address)
        form.fields['route'].widget.attrs['placeholder'] = 'ej: gran via'
        form.fields['street_number'].widget.attrs['placeholder'] = 'ej: 18'
        form.fields['postal_code'].widget.attrs['placeholder'] = 'ej: 28020'
    return render_to_response('location.html', {'form': form, 'room_id': room_id, 'messages': message}, RequestContext(request))


def location_map(request, room_id):
    if request.is_ajax():
        if request.method == 'GET':
            room = Room.objects.get(id=room_id)
            lat = room.location.lat
            lng = room.location.lng
            return JsonResponse({'latlng': [lat, lng]})
        elif request.method == 'POST':
            room = Room.objects.get(id=room_id)
            lat = request.POST['lat']
            lng = request.POST['lng']
            print(lat)
            if lat != "":
                g = geocoder.google([lat, lng], method='reverse')
                print(g.json)
                if g.ok and g.postal == room.location.postal_code:
                    room.location.lat = lat
                    room.location.lng = lng
                    # room.location.route = g.street
                    # room.location.street_number = g.housenumber
                    room.location.save()
            return JsonResponse({'ok': 200})


def amenities(request, room_id):
    room = Room.objects.get(id=room_id)
    message = convert_message_to_toastr(messages.get_messages(request))
    try:
        amenity = room.amenity
    except Amenity.DoesNotExist:
        amenity = Amenity(room=room)
    if request.method == 'POST':
        form = AmenityForm(request.POST, instance=amenity)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'edit your amenities successfully!')
            return HttpResponseRedirect(reverse('spaces', kwargs={'room_id': room_id}))
    else:
        form = AmenityForm(instance=amenity)
    return render_to_response('amenity.html', {'form': form, 'room_id': room_id, 'messages': message}, RequestContext(request))


def spaces(request, room_id):
    message = convert_message_to_toastr(messages.get_messages(request))
    room = Room.objects.get(id=room_id)
    try:
        space = room.spaceshare
    except SpaceShare.DoesNotExist:
        space = SpaceShare(room=room)
    if request.method == 'POST':
        form = SpaceShareForm(request.POST, instance=space)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'edit your spaces successfully!')
            return HttpResponseRedirect(reverse('room_section', kwargs={'room_id': room_id}))
    else:
        form = SpaceShareForm(instance=space)
    return render_to_response('space.html', {'form': form, 'room_id': room_id, 'messages': message}, RequestContext(request))


def photos(request, room_id):
    message = convert_message_to_toastr(messages.get_messages(request))
    room = Room.objects.get(id=room_id)
    try:
        photo = room.photo
    except Photo.DoesNotExist:
        photo = Photo(room=room)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'edit your photos successfully!')
            return HttpResponseRedirect(reverse('highlights', kwargs={'room_id': room_id}))
    else:
        form = PhotoForm(instance=photo)
    return render_to_response('photos.html', {'form': form, 'room_id': room_id, 'messages': message}, RequestContext(request))


def highlights(request, room_id):
    message = convert_message_to_toastr(messages.get_messages(request))
    room = Room.objects.get(id=room_id)
    try:
        high = room.highlight
    except HighLight.DoesNotExist:
        high = HighLight(room=room)
    if request.method == 'POST':
        form = HighLightForm(request.POST, instance=high)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'edit your highlights successfully!')
            return HttpResponseRedirect(reverse('name_description', kwargs={'room_id': room_id}))
    else:
        form = HighLightForm(instance=high)
    return render_to_response('highlight.html', {'form': form, 'room_id': room_id, 'messages': message}, RequestContext(request))


def name_description(request, room_id):
    message = convert_message_to_toastr(messages.get_messages(request))
    room = Room.objects.get(id=room_id)
    try:
        name = room.namedescription
    except NameDescription.DoesNotExist:
        name = NameDescription(room=room)
    if request.method == 'POST':
        form = NameDescriptionForm(request.POST, instance=name)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'edit your name and description successfully!')
            return HttpResponseRedirect(reverse('room_section', kwargs={'room_id': room_id}))
    else:
        form = NameDescriptionForm(instance=name)
    return render_to_response('name_description.html', {'form': form, 'room_id': room_id, 'messages': message}, RequestContext(request))


def calenders(request, room_id):
    message = convert_message_to_toastr(messages.get_messages(request))
    room = Room.objects.get(id=room_id)
    try:
        calender = room.calender
    except Calender.DoesNotExist:
        calender = Calender(room=room)
    if request.method == 'POST':
        form = CalenderForm(request.POST, instance=calender)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'edit your calender successfully!')
            return HttpResponseRedirect(reverse('price', kwargs={'room_id': room_id}))
    else:
        form = CalenderForm(instance=calender)
    return render_to_response('calender.html', {'form': form, 'room_id': room_id, 'messages': message}, RequestContext(request))


def price(request, room_id):
    message = convert_message_to_toastr(messages.get_messages(request))
    room = Room.objects.get(id=room_id)
    try:
        p = room.price
    except Price.DoesNotExist:
        p = Price(room=room)
    if request.method == 'POST':
        form = PriceForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'edit your calender successfully!')
            return HttpResponseRedirect(reverse('room_section', kwargs={'room_id': room_id}))
    else:
        form = PriceForm(instance=p)
    return render_to_response('price.html', {'form': form, 'room_id': room_id, 'messages': message}, RequestContext(request))


@login_required()
def rooms(request, room_id):
    message = convert_message_to_toastr(messages.get_messages(request))
    if request.method == 'GET':
        room = Room.objects.get(id=room_id)
        zip = room.location.postal_code
        geo = {
            'lat': room.location.lat,
            'lng': room.location.lng
        }
        room_nearby = Location.objects.filter(postal_code__exact=zip)
        context = {
            'room': room,
            'geo': json.dumps(geo),
            'room_nearby': room_nearby,
            'form': ReservationForm(),
            'messages': message
        }
        return render_to_response('room.html', context, RequestContext(request))
    if request.is_ajax():
        if request.method == 'DELETE':
            try:
                room = Room.objects.get(id=room_id)
                room.delete()
            except Room.DoesNotExist:
                raise 404
            other_rooms = request.user.room_set.all()
            template = render_to_response('room_list_view.html', {'rooms': other_rooms})
            return HttpResponse(template)


def active(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.is_ajax():
        if request.method == 'POST':
            if request.POST['active'] == 'Active':
                room.is_active = True
            else:
                room.is_active = False
            room.save()
        return JsonResponse({'ok': 200})


