# Generated by Django 3.2 on 2021-10-03 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20211003_0647'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='phone',
            field=models.CharField(default='', max_length=16),
        ),
    ]
