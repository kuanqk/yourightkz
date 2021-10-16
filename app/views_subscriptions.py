import datetime
import random

from django.shortcuts import render, redirect, HttpResponse
from app.models import Subscription, Profile


def index(request):
    if request.user.is_anonymous:
        return redirect("/login.html")

    try:
        if not request.user.profile.sms_ok:
            return redirect("/sms.html")
    except:
        pass

    context = {"subscriptions": Subscription.objects.filter(user=request.user).order_by("-id")}

    return render(request, "subscriptions.html", context=context)


def add(request):
    if request.user.is_anonymous:
        return redirect("/login.html")

    if request.method == "POST":
        subs = Subscription()
        subs.user = request.user
        subs.first_name = request.POST.get("firstname", "")
        subs.last_name = request.POST.get("lastname", "")
        subs.phone = request.POST.get("phone", "")
        subs.iin = request.POST.get("iin", "")
        subs.license_plate = request.POST.get("license_plate", "")
        subs.save()
        subs.transaction_id = subs.id*10000 + random.randint(100, 9999)
        subs.save()
        return redirect(f"/subscriptions/{subs.id}/pay/")
    else:
        subs = Subscription()
        subs.last_name = request.user.last_name
        subs.first_name = request.user.first_name
        subs.phone = request.user.username

        try:
            profile = Profile.objects.get(user=request.user)
            subs.iin = profile.iin
        except:
            pass

        context = {"subs": subs}

        return render(request, "subscriptions_add.html", context=context)


def pay(request, id):
    if request.user.is_anonymous:
        return redirect("/login.html")

    subs = Subscription.objects.get(id=id)
    if subs.user != request.user:
        return redirect("/404.html")

    if request.method == "POST":
        print("Tried to really pay :)")

    context = {"subs": subs}
    if not subs.paid:
        return render(request, "subscriptions_pay.html", context=context)

    context["today"] = datetime.datetime.today().date()
    return render(request, "subscriptions_thank_you.html", context=context)


def apply_payment(request, id, transaction_id):
    subs = Subscription.objects.get(id=id)
    if subs.transaction_id == transaction_id:
        subs.paid = True
        subs.active = True
        subs.valid_from = datetime.datetime.today().date() + datetime.timedelta(days=1)
        subs.valid_to = datetime.date(
            year=subs.valid_from.year+1,
            day=subs.valid_from.day,
            month=subs.valid_from.month
        ) + datetime.timedelta(days=-1)
        subs.save()
        return HttpResponse("OK")
    return redirect("/404.html")
