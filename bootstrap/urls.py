"""student URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bootstrap import settings
from django.conf.urls.static import static
from app import views
import app.views_registration as view_registration
import app.views_subscriptions as view_subscriptions

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sms_again.html", view_registration.sms_again),
    path("sms.html", view_registration.sms),
    path("register.html", view_registration.register),
    path("subscriptions.html", view_subscriptions.index),
    path("subsriptions/add/", view_subscriptions.add),
    path("<filename>.html", views.html),
    path("", views.index),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
