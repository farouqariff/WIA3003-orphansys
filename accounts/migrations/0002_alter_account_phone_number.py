# Generated by Django 4.1.4 on 2022-12-28 16:42

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                max_length=16, region=None, unique=True
            ),
        ),
    ]
