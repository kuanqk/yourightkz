import requests
from app.models import Property


prod_server_url = "https://api-core.wooppay.com/v1"

def login():
    r = requests.post(
        f"{prod_server_url}/auth",
        json={
            "login": "yurrait",
            "password": "5oGv1b3AsT",
        }
    )
    return r.json()["token"]


def invoice(token, subs):
    amount = 2000
    try:
        amount = int(Property.objects.get(key="price").value)
    except Exception as e:
        pass

    r = requests.post(
        f"{prod_server_url}/invoice/create",
        headers={'Authorization': token},
        json={
            "amount": amount,
            "reference_id": str(subs.transaction_id),
            "merchant_name": "yurrait",
            "request_url": {
                "url": f"https://c.youright.kz/subscriptions/{subs.id}/apply_payment/{subs.transaction_id}",
                "type": "GET"},
            "user_phone": subs.phone,
            "email": subs.user.email,
            "back_url": f"https://c.youright.kz/subscriptions/{subs.id}/pay/",
            "description": "Подписка на 1 год",
            "option": "4"
        }
    )
    print(r.json())
    return r.json()["operation_url"]
