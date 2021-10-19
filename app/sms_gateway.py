from app.models import Property
import requests
from threading import Thread


class SmsThread(Thread):
    def __init__(self, phone, text):
        self.phone = phone
        self.text = text
        Thread.__init__(self)

    def run(self):
        phone = self.phone.replace(" ", "")
        ok = False
        if phone[:2] == "+7":
            ok = True
        elif phone[0] == "8":
            ok = True
            phone = "+7" + phone[1:]
        elif len(phone) == 10:
            ok = True
            phone = "+7" + phone
        if ok:
            mobizon_api = Property.objects.get(key="mobizon_api")
            mobizon_key = Property.objects.get(key="mobizon_key")
            r = requests.get(f"https://{mobizon_api.value}/service/Message/SendSmsMessage?"
                             f"output=json&apiKey={mobizon_key.value}&"
                             f"from=YouRight&"
                             f"recipient={phone}&text={self.text}")
            return r.content.decode("utf-8")


def send_sms(phone, text):
    SmsThread(phone, text).start()
