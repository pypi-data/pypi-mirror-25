from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# Check app configuration
APPODEAL_REWARD_CREATE_HANDLER = getattr(settings, 'APPODEAL_REWARD_CREATE_HANDLER', None)

if not APPODEAL_REWARD_CREATE_HANDLER:
    raise ImproperlyConfigured('You need to define APPODEAL_REWARD_CREATE_HANDLER')

APPODEAL_SECRET_ANDROID = getattr(settings, 'APPODEAL_SECRET_ANDROID', None)
APPODEAL_SECRET_IOS = getattr(settings, 'APPODEAL_SECRET_IOS', None)

if not any((APPODEAL_SECRET_ANDROID, APPODEAL_SECRET_IOS)):
    raise ImproperlyConfigured('You need at least one of APPODEAL_SECRET_ANDROID  APPODEAL_SECRET_IOS')


class Reward(models.Model):
    # Data sent by Appodeal
    data1 = models.TextField(default='')
    data2 = models.TextField(default='')

    # Decyphered content for faster access
    output = models.TextField(default='')
    user_id = models.TextField(default='')
    amount = models.TextField(default='')
    currency = models.TextField(default='')
    impression_id = models.TextField(default='')
    timestamp = models.TextField(default='')
    hash = models.TextField(default='')

    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
