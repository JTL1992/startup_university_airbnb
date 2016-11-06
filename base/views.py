import geocoder
from django.http import JsonResponse
from django.shortcuts import render, render_to_response
from django.contrib import messages
import logging
import json
from helper import convert_message_to_toastr, add_notification
# Create your views here.
from django.template import Context, RequestContext

from rooms.models import Room

logger = logging.getLogger('base')


def home(request):
    message = convert_message_to_toastr(messages.get_messages(request))
    rooms = Room.objects.all().filter(is_active=True)
    return render_to_response('home.html', {'messages': message, 'rooms': rooms}, RequestContext(request))
