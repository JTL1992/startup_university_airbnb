import hashlib
import urllib

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


def get_user_avatar(user):
    if user.socialaccount_set.all().count():
        img_url = user.socialaccount_set.all()[0].get_avatar_url()
    else:
        default = "https://example.com/static/images/defaultavatar.jpg"
        img_url = "https://www.gravatar.com/avatar/%s?%s" % \
                  (hashlib.md5(user.email.lower()).hexdigest(), urllib.urlencode({'d': default, 's': str(100)}))
    return img_url

