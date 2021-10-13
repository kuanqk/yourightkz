from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import ObjectDoesNotExist
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

    subs = Subscription.objects.get(id=int(id))

    context = {"subs": subs}

    return render(request, "subscriptions_pay.html", context=context)
