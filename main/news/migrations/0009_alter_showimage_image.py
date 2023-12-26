# Generated by Django 4.2.7 on 2023-12-17 13:53

from django.db import migrations, models
import news.models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0008_alter_showimage_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="showimage",
            name="image",
            field=models.ImageField(upload_to=news.models.ShowImage.folder_path),
        ),
    ]
