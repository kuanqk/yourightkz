from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import ObjectDoesNotExist
from app.models import Subscription


def index(request):
    if request.user.is_anonymous:
        return redirect("/login.html")

    context = {"subscriptions": Subscription.objects.filter(user=request.user)}

    return render(request, "subscriptions.html", context=context)
