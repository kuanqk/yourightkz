from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import ObjectDoesNotExist


def error(request, error_text):
    context = {"error": error_text}
    return render(request, "register.html", context=context)


def clean_phone_number(phone):
    phone = phone.replace(" ", "").replace("+7", "8")
    # TODO: filter out by numbers only

    return phone

def register(request):
    context = {"error": ""}
    print("request method", request.method)
    if request.method == "POST":
        phone = clean_phone_number(request.POST.get("phone", ""))
        first_name = request.POST.get("firstname", "")
        last_name = request.POST.get("lastname", "")
        password = request.POST.get("password", "")
        repeat_password = request.POST.get("repeat_password", "")
        if len(phone) < 10:
            return error(request, "Пожалуйста, введите номер телефона")
        if len(first_name) < 2:
            return error(request, "Пожалуйста, введите имя")
        if len(last_name) < 2:
            return error(request, "Пожалуйста, введите фамилию")
        if len(password) < 8:
            return error(request, "Пожалуйста, введите пароль, минимум 8 символов")
        if password != repeat_password:
            return error(request, "Пароли не совпадают")
        if User.objects.filter(id=phone).exists():
            return error(request, "Пользователь с таким номером телефона уже существует")

        user = User()
        user.username = phone
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save()

        login(request, user)
        return redirect("/index.html")

    return render(request, "register.html", context=context)
