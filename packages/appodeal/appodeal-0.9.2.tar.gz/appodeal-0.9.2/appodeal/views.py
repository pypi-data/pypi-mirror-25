from Crypto.Cipher import AES
import codecs
import hashlib
import urllib.parse

from django.conf import settings
from django.views.generic import View
from django.http import HttpResponse

from appodeal import models


class RewardCreateAPIView(View):
    """Callback from Appodeal with data1 and data2 parameters. Always
    returns HTTP 201.

    """
    # Intentionally no authentication or permission beacuse it's
    # called from a provider.
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        data1 = request.GET.get('data1')
        data2 = request.GET.get('data2')
        if data1 is not None and data2 is not None:
            # Get result for iOS and Android
            output = {}
            output_ios, output_android = request_is_valid(data1, data2, models.APPODEAL_SECRET_ANDROID), request_is_valid(data1, data2, models.APPODEAL_SECRET_IOS)
            # Get the valid output or `None`
            output = isinstance(output_ios, dict) and output_ios or isinstance(output_android, dict) and output_android or None
            # If we got a valid output
            if output is not None:
                try:
                    result = models.APPODEAL_REWARD_CREATE_HANDLER
                except Exception as e:
                    result = str(e)
            # If both outputs are bad
            else:
                result = 'iOS: ' + str(output_ios) + '\n' + 'Android: ' + str(output_android)
                output = {}
            reward = models.Reward(**output)
            reward.data1 = data1
            reward.data2 = data2
            reward.result = result
            reward.save()

        return HttpResponse(status=201)


def request_is_valid(data1, data2, key):
    output = None
    try:
        key = hashlib.sha256(key.encode('utf-8')).digest()
        # Verify and reward user

        def unpad(s):
            return s[0:-ord(s[-1])]
        # Encryption key you set for the app in dashboard
        # Decrypting data1 and data2
        iv = codecs.decode(data1, 'hex_codec')
        encrypted = codecs.decode(data2, 'hex_codec')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(encrypted).decode('utf-8'))
        output = urllib.parse.parse_qs(decrypted)
        # User ID set using Appodeal.getUserSettings(this).setUserId("User#123") method in your app
        user_id = output['user_id'][0]
        # Reward amount
        amount = output['amount'][0]
        # Reward currency
        currency = output['currency'][0]
        # Unique impression ID in the UUID form
        impression_id = output['impression_id'][0]
        # Timestamp of the impression
        timestamp = output['timestamp'][0]
        # Hash of the data used for validity confirmation
        hash = output['hash'][0]
        # Hash of the data calculation
        the_string = "user_id=%s&amount=%s&currency=%s&impression_id=%s&timestamp=%s"
        hash_string = hashlib.sha1((the_string % (user_id, amount, currency, impression_id, timestamp)).encode('utf-8')).hexdigest()
        # If hashes match impression is valid
        if hash.upper() == hash_string.upper():
            output = {
                'user_id': user_id,
                'amount': amount,
                'currency': currency,
                'impression_id': impression_id,
                'timestamp': timestamp,
                'hash': hash,
                'output': output
            }
    except Exception as e:
        output = str(e)
    return output
