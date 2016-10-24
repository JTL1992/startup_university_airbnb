from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth.models import User
import logging

from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import get_adapter as get_account_adapter
logger = logging.getLogger('accounts')


class AccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        try:
            print('AccountAdapter run!!!!')
            user = User.objects.get(email=sociallogin.email_addresses)
            logger.info('this is email !!!!!!!!!!!!!')
            sociallogin.connect(request, user)
            login(request, user)
            response = 'My Adapter pre_social_login'
            raise ImmediateHttpResponse(response)
        except User.DoesNotExist:
            pass
