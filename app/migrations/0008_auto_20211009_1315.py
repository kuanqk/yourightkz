# Generated by Django 3.2 on 2021-10-09 13:15

from django.db import migrations
from app.models import Property


def create_mobizon_credentials(apps, schema_editor):
    prop = Property()
    prop.key = "mobizon_api"
    prop.value = "api.mobizon.kz"
    prop.save()
    prop = Property()
    prop.key = "mobizon_key"
    prop.value = "kz63ae503eed663cc235fd0935b15e8df0e330323543892913f8332a0d11a3b52d8cef"
    prop.save()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_property'),
    ]

    operations = [
        migrations.RunPython(create_mobizon_credentials, migrations.RunPython.noop)
    ]