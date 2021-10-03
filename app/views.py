from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import ObjectDoesNotExist
from app.views_registration import clean_phone_number


def index(request):
    if request.user.is_anonymous:
        return redirect("/login.html")
    return html(request, "index")


def html(request, filename):
    context = {"filename": filename, "collapse": ""}
    if request.user.is_anonymous and filename not in ["login", "register"]:
        return redirect("/login.html")
    if not request.user.is_anonymous:
        context["last_name"] = request.user.last_name
        context["first_name"] = request.user.first_name
    if filename == "logout":
        logout(request)
        return redirect("/")
    if filename == "login" and request.method == "POST":
        username = clean_phone_number(request.POST.get("phone", ""))
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                context["error"] = "Wrong password"
        except ObjectDoesNotExist:
            context["error"] = "User not found"

        print("login")
        print(username, password)
    print(filename, request.method)
    if filename in ["buttons", "cards"]:
        context["collapse"] = "components"
    if filename in [
        "utilities-color",
        "utilities-border",
        "utilities-animation",
        "utilities-other",
    ]:
        context["collapse"] = "utilities"
    if filename in ["404", "blank"]:
        context["collapse"] = "pages"

    return render(request, f"{filename}.html", context=context)
