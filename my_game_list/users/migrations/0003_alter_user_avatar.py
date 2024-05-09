# Generated by Django 4.2.4 on 2024-05-09 08:17

from django.db import migrations, models
import my_game_list.my_game_list.validators.file_size_validator


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_user_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="avatars/",
                validators=[my_game_list.my_game_list.validators.file_size_validator.FileSizeValidator()],
                verbose_name="avatar",
            ),
        ),
    ]
