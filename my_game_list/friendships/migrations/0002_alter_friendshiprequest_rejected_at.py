# Generated by Django 4.1.7 on 2023-03-22 18:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("friendships", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="friendshiprequest",
            name="rejected_at",
            field=models.DateTimeField(blank=True, null=True, verbose_name="rejection time"),
        ),
    ]
