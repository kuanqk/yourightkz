from django.db import models
from django.contrib.auth.models import User


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    type = models.CharField(max_length=100, default="personal")
    tarif = models.CharField(max_length=100, default="personal")
    valid_from = models.DateField(blank=False, null=False)
    valid_to = models.DateField(blank=False, null=False)
    license_plate = models.CharField(max_length=16, blank=False, null=False)
    json_data = models.CharField(max_length=1000, default="{}")
    iin = models.CharField(max_length=12, default="")
    active = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    # payment_status = models.CharField(max_length=100, default="Init")

    def __str__(self):
        active = "НЕАКТИВНАЯ"
        if self.active:
            active = "АКТИВНАЯ"

        paid = "НЕ ОПЛАЧЕНО"
        if self.paid:
            paid = "ОПЛАЧЕНО"

        return f"{self.user.last_name}, {self.iin}, {self.valid_from}, {active}, {paid}"


class Incident(models.Model):
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, null=False, blank=False
    )
    date = models.DateField(blank=False, null=False)
    json_data = models.CharField(max_length=1000, default="{}")
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, default="initiated")

    def __str__(self):
        return f"{self.subscription.iin}: {self.description}"
