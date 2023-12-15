# Generated by Django 4.2.7 on 2023-12-13 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_alter_account_account_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="account_image",
            field=models.ImageField(
                default="account_images/default_account.png",
                upload_to="account_images",
                verbose_name="Изображение профиля",
            ),
        ),
    ]
