# Generated by Django 3.2 on 2021-10-03 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20211003_0640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='valid_from',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='valid_to',
            field=models.DateField(blank=True, null=True),
        ),
    ]
