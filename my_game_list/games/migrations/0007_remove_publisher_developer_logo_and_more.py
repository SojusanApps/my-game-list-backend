# Generated by Django 4.2.4 on 2024-06-11 08:08

from django.db import migrations, models
import my_game_list.my_game_list.validators.file_size_validator


class Migration(migrations.Migration):
    dependencies = [
        ("games", "0006_developer_developer_logo_publisher_developer_logo"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="publisher",
            name="developer_logo",
        ),
        migrations.AddField(
            model_name="publisher",
            name="publisher_logo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="publisher_logo/",
                validators=[my_game_list.my_game_list.validators.file_size_validator.FileSizeValidator()],
                verbose_name="developer logo",
            ),
        ),
        migrations.AlterField(
            model_name="developer",
            name="developer_logo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="developer_logo/",
                validators=[my_game_list.my_game_list.validators.file_size_validator.FileSizeValidator()],
                verbose_name="developer logo",
            ),
        ),
    ]
