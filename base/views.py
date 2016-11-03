import geocoder
from django.http import JsonResponse
from django.shortcuts import render, render_to_response
from django.contrib import messages
import logging
import json
from helper import convert_message_to_toastr, add_notification
# Create your views here.
from django.template import Context

logger = logging.getLogger('base')


def home(request):
    g = geocoder.google([40.3888543, -3.7328683], method='reverse')
    print(g.json)
    message = convert_message_to_toastr(messages.get_messages(request))
    return render_to_response('home.html', {'user': request.user, 'messages': message})
