# Generated by Django 5.1.6 on 2025-02-10 23:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0012_alter_gamemedia_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="gamefollow",
            options={"ordering": ("id",), "verbose_name": "game follow", "verbose_name_plural": "games follows"},
        ),
    ]
