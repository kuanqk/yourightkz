import datetime

from django.db import models
from django.contrib.auth.models import User


class Property(models.Model):
    key = models.CharField(max_length=100, null=False, blank=False)
    value = models.CharField(max_length=1000, null=False, blank=False)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name_plural = "Properties"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iin = models.CharField(max_length=12, default="")
    sms_code = models.CharField(max_length=100, default="1233212")
    sms_ok = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    type = models.CharField(max_length=100, default="personal")
    tarif = models.CharField(max_length=100, default="personal")
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    license_plate = models.CharField(max_length=16, blank=False, null=False)
    json_data = models.CharField(max_length=1000, default="{}")
    iin = models.CharField(max_length=12, default="")
    phone = models.CharField(max_length=16, default="")
    last_name = models.CharField(max_length=100, default="")
    first_name = models.CharField(max_length=100, default="")
    active = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    transaction_id = models.IntegerField(default=0)
    # payment_status = models.CharField(max_length=100, default="Init")

    def is_valid(self):
        if self.valid_from is None or self.valid_to is None:
            return False
        today = datetime.datetime.today().date()
        return self.valid_from <= today <= self.valid_to

    def __str__(self):
        active = "НЕАКТИВНАЯ"
        if self.active:
            active = "АКТИВНАЯ"

        paid = "НЕ ОПЛАЧЕНО"
        if self.paid:
            paid = "ОПЛАЧЕНО"

        return f"{self.last_name} {self.first_name}, {self.iin}, {self.valid_from}, {active}, {paid}"


class Process(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    status = models.CharField(max_length=1000, default="Открыт")

    def __str__(self):
        return


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
