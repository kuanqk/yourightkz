from app.models import Property
import requests


def send_sms(phone, text):
    phone = phone.replace(" ", "")
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
                         f"recipient={phone}&text={text}")

        return r.content.decode("utf-8")
