# Generated by Django 4.1.4 on 2022-12-30 09:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("donor", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256)),
                ("rqd", models.IntegerField(blank=True, default=0)),
                ("date", models.DateField(blank=True, default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name="ItemDonation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("qty", models.IntegerField()),
                ("date", models.DateField(default=datetime.date.today)),
                (
                    "donor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="donor.donor"
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="donation.item"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CashDonation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amt", models.IntegerField()),
                ("receipt", models.ImageField(upload_to="receipts/")),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[
                            ("", "Select"),
                            (1, "Unreceived"),
                            (2, "Pending"),
                            (3, "Received"),
                        ],
                        default=2,
                    ),
                ),
                ("date", models.DateField(default=datetime.date.today)),
                (
                    "donor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="donor.donor"
                    ),
                ),
            ],
        ),
    ]
