from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response
from allauth.account.views import *
from django.template import RequestContext
from base.helper import add_notification, convert_message_to_toastr, get_user_avatar
from django.views.decorators.csrf import csrf_protect
from models import UserProfile
from forms import UserForm
from django.contrib import messages
from django.core.urlresolvers import reverse
import hashlib
import urllib

# Create your views here.


@csrf_protect
@login_required()
def my_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            save_user(user=user, form=form)
            save_profile(user=user, form=form)
            messages.add_message(request, messages.SUCCESS, 'update user information successfully')
        else:
            messages.add_message(request, messages.ERROR, 'update user information unsuccessfully')
        return HttpResponseRedirect(reverse('public_profile', kwargs={'user_id': user.id}))
    else:
        phone = ''
        description = ''
        if user.userprofile_set.count():
            phone = user.userprofile_set.get().phone
            description = user.userprofile_set.get().description
        form = UserForm(initial={
            'username': user.username,
            'email': user.email,
            'phone': phone,
            'description': description,
            })
    return render_to_response('my_profile.html', {'user': request.user, 'form': form}, RequestContext(request))


def save_user(user, form):
    profile = form.cleaned_data
    user.username = profile['username']
    user.email = profile['email']
    user.save()


def save_profile(user, form):
    profile = form.cleaned_data
    if user.userprofile_set.count():
        user_profile = user.userprofile_set.get()
        user_profile.description = profile['description']
        user_profile.phone = profile['phone']
        user_profile.image_url = get_user_avatar(user)
        user_profile.save()
    else:
        new_profile = UserProfile(user=user, phone=profile['phone'], description=profile['description'],
                                  image_url=get_user_avatar(user))
        new_profile.save()


@login_required()
def public_profile(request, user_id):
    user = User.objects.get(id=user_id)
    message = convert_message_to_toastr(messages.get_messages(request))
    profile = user.userprofile_set.get()
    return render_to_response('public_profile.html', {'user': user, 'messages': message, 'profile': profile})
