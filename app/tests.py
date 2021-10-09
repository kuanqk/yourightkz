from django.test import TestCase
from app.sms_gateway import send_sms


class TestEverything(TestCase):
    def a_test_sms(self):
        content = send_sms("+77789711555", "test sms")
        self.assertTrue('"code":0' in content)
