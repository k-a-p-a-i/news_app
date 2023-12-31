# Generated by Django 4.2.7 on 2023-11-23 21:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("news", "0005_category_alter_article_date_article_category"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="article",
            options={
                "ordering": ["title", "date"],
                "verbose_name": "Новость",
                "verbose_name_plural": "Новости",
            },
        ),
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "Категория", "verbose_name_plural": "Категории"},
        ),
        migrations.AddField(
            model_name="article",
            name="image",
            field=models.ImageField(
                blank=True,
                upload_to="article/<function Article.show_id at 0x00000202AEF21120>",
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="news.category",
                verbose_name="Категория",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                help_text="Введите категорию новости",
                max_length=200,
                unique=True,
                verbose_name="Категория",
            ),
        ),
    ]
