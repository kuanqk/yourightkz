from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import ObjectDoesNotExist
from app.sms_gateway import send_sms
from app.models import Profile
import random


def error(request, error_text):
    context = {"error": error_text}
    return render(request, "register.html", context=context)


def clean_phone_number(phone):
    phone = phone.replace(" ", "").replace("+7", "8").replace('-','')
    # TODO: filter out by numbers only

    return phone


def sms_again(request):
    if request.user.is_anonymous:
        return redirect("/login.html")
    if request.user.profile.sms_ok:
        return redirect("/subscriptions.html")
    send_sms(request.user.username, f"Код регистрации на youright.kz: {request.user.profile.sms_code}")
    return redirect("/sms.html")


def sms(request):
    if request.user.is_anonymous:
        return redirect("/login.html")
    if request.user.profile.sms_ok:
        return redirect("/subscriptions.html")
    context = dict()
    if request.method == "POST":
        if request.POST.get("sms_code", "") == request.user.profile.sms_code:
            request.user.profile.sms_ok = True
            request.user.profile.save()
            return redirect("/subscriptions.html")
        else:
            context["error"] = "Код неверный"
    return render(request, "register_sms.html", context=context)


def register(request):
    context = {"error": ""}
    print("request method", request.method)
    if request.method == "POST":
        phone = clean_phone_number(request.POST.get("phone", ""))
        first_name = request.POST.get("firstname", "")
        last_name = request.POST.get("lastname", "")
        password = request.POST.get("password", "")
        repeat_password = request.POST.get("repeat_password", "")
        if len(phone) < 10 and phone.isnumeric():
            return error(request, "Пожалуйста, введите номер телефона")
        if len(first_name)< 2:
            return error(request, "Пожалуйста, введите имя")
        if len(last_name) < 2:
            return error(request, "Пожалуйста, введите фамилию")
        if len(password) < 6:
            return error(request, "Пожалуйста, введите пароль, минимум 6 символов")
        if password != repeat_password:
            return error(request, "Пароли не совпадают")
        if User.objects.filter(username=phone).exists():
            return error(
                request, "Пользователь с таким номером телефона уже существует"
            )

        user = User()
        user.username = phone
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save()

        profile = Profile()
        profile.user = user
        profile.sms_code = str(random.randint(1000, 9999))
        profile.save()

        send_sms(profile.user.username, f"Код регистрации на youright.kz: {profile.sms_code}")

        login(request, user)
        return redirect("/sms.html")

        # return redirect("/index.html")

    return render(request, "register.html", context=context)
