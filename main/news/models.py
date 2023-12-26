from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import shutil
import os



from django.conf import settings

base_dir = settings.MEDIA_ROOT

import datetime
class PublishedToday(models.Manager):
    def get_queryset(self):
        return super(PublishedToday,self).get_queryset().filter(date__gte=datetime.date.today())

class Tag(models.Model):
    title = models.CharField(max_length=15, verbose_name='Название')
    status = models.BooleanField(default=True, verbose_name='Статус')

    def __str__(self):
        return self.title

    def tag_count(self):
        count = self.article_set.count()
        return count

    class Meta:
        ordering = ['title', 'status']
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"



class Article(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Автор')
    title = models.CharField('Название', max_length=50, default='')
    anouncement = models.TextField('Аннотация', max_length=250)
    text = models.TextField('Текст новости')
    date = models.DateTimeField('Дата публикации', auto_now=True) #default=timezone.now
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    tags = models.ManyToManyField(to = Tag, blank=True, verbose_name='Тэги')


    objects = models.Manager()
    published = PublishedToday()

    #date_created = models.DateTimeField(auto_now_add=True)
    #date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Новость: {self.title} от {str(self.date)[:19]}'
    def get_absolute_url(self):
        return f'/news/{int(self.id)}'
    def tag_list(self):
        s = ''
        for tag in self.tags.all():
            s += '*'+tag.title +' '
        return s

    def image_tag(self):
        image = ShowImage.objects.filter(article = self)
        if image:
            return mark_safe(f"<img src='{image[0].image.url}' height='50px' width='auto'/>")
        else:
            return 'No Image'


    def delete(self, *args, **kwargs):
        """для автоматического удаления папки с изображениями статьи"""
        dir_path = f"article_images/article_{self.pk}"
        ar_dir = os.path.join(base_dir, dir_path)
        if os.path.exists(ar_dir):
            shutil.rmtree(ar_dir)

        super(Article, self).delete(*args, **kwargs)

    def get_views(self):
        return self.views.count() #views - это related_name из связанной модели ViewCounter

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['title','date']



class Category(models.Model):
    name = models.CharField('Категория', max_length=200,
                            unique=True,
                            )

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"



class ShowImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=True)

    def folder_path(instance, filename):
        return f"article_images/article_{instance.article.pk}/{filename}"

    image = models.ImageField(upload_to=folder_path)

    def __str__(self):
        return self.title
    def image_tag(self):
        if self.image is not None:
            return mark_safe(f"<img src='{self.image.url}' height='50px' width='auto'/>")
        else:
            return 'No Image'

##-----------------------Счетчик просмотров_________________________#######################
class ViewCounter(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='views', verbose_name='Счетчик просмотров')
    ip_address = models.GenericIPAddressField()
    view_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-view_date", )
        indexes = [models.Index(fields=["-view_date",])]

    def __str__(self):
        return self.article.title