# Generated by Django 4.2.4 on 2024-06-11 09:18

from django.db import migrations, models
import my_game_list.my_game_list.validators.file_size_validator


class Migration(migrations.Migration):
    dependencies = [
        ("games", "0007_remove_publisher_developer_logo_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="developer",
            name="developer_logo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="developer_logos/",
                validators=[my_game_list.my_game_list.validators.file_size_validator.FileSizeValidator()],
                verbose_name="developer logo",
            ),
        ),
        migrations.AlterField(
            model_name="publisher",
            name="publisher_logo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="publisher_logos/",
                validators=[my_game_list.my_game_list.validators.file_size_validator.FileSizeValidator()],
                verbose_name="developer logo",
            ),
        ),
    ]
