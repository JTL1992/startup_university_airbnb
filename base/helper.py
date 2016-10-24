from django.contrib import messages
import json


def add_notification(request, level, message):
    messages.add_message(request, level, message)
    return convert_message_to_toastr(messages.get_messages(request))


def convert_message_to_toastr(message):
    messages_list = []
    for m in message:
        messages_list.append({'msg': m.message, 'tag': m.tags})
    return json.dumps(messages_list)

