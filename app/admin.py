from django.contrib import admin
from app.models import Subscription, Incident, Profile, Property


class SubscriptionAdmin(admin.ModelAdmin):
    ordering = ["-id"]
    search_fields = ["last_name", "first_name", "iin", "valid_from", "valid_to"]
    list_filter = ["active", "valid_from", "valid_to"]


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Incident)
admin.site.register(Profile)
admin.site.register(Property)

admin.site.site_header = "Панель администратора YouRight"
admin.site.site_title = "Панель администратора YouRight"
admin.site.index_title = "Добро пожаловать в YouRight"
