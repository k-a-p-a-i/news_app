from django.db import models
from django.contrib.auth.models import User


from django.dispatch import receiver
from django.db.models.signals import post_save

class Account(models.Model):
    gender_choices = (
        ('M', 'Мужской'),
        ('Ж', 'Женский'),
        ('Н/Д', 'не указано')
            )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='Пользователь')
    birthdate = models.DateField( verbose_name="Дата рождения")
    gender = models.CharField(choices=gender_choices, max_length=20, verbose_name="Пол")

    def folder_path(instance, filename):
        return f"account_images/{instance.user.username}/{filename}"


    account_image = models.ImageField(default='account_images/default_account.png', upload_to=folder_path, verbose_name="Изображение профиля")


    def __str__(self):
        return f"{self.user.username}'s account"

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Account.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.account.save()



    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

