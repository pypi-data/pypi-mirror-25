from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from appodeal import models


class RewardCreateAPIViewTestCase(TestCase):
    def test_success(self):
        User.objects.create(username='AF')
        url = reverse('appodeal:reward-create')
        # From their example code
        data1 = "02A87383F97008D2F8898DA81A39EDAF"
        data2 = "839EA3731891B24D8025F447747F097664DB4F6A1B88351796EFF7234BE99B21A8E6176F7515C0E4520E898BE97F1B50D48F9979DE6B96822CA9E4DAB6094076E71A2898DC22632FEE638F611334B08557964783B9F98C10D2B841C2182ED5F707F569143431847800EDA5C0D2FFE8BC2550D4F16850F57DBE4315404D10BA295D724A30BB3B2FB6FB72F74624819D5F89AEFB73E8C8EE0D61E8224E749C6BC8"
        data = {'data1': data1, 'data2': data2}

        response = self.client.get(url, data)

        self.assertEqual(response.status_code, 201)
        obj = models.Reward.objects.get()
        self.assertEqual(obj.result, 'Rewarded with 100')
