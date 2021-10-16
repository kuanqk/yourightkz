import random

from django.test import TestCase
from app.sms_gateway import send_sms
from app.models import Subscription
from django.contrib.auth.models import User
from app.woopay import login, invoice


class TestEverything(TestCase):
    def a_test_sms(self):
        content = send_sms("+77789711555", "test sms")
        self.assertTrue('"code":0' in content)

    def test_login_to_wooppay(self):
        user = User()
        user.email = "test@gmail.com"
        user.username = "testuser"
        token = login()
        subs = Subscription()
        subs.phone = "7771112223"
        subs.user = user
        subs.transaction_id = 9999 + random.randint(0,1000000)
        subs.id = 7
        url = invoice(token, subs)
        assert url[:5] == "https"
