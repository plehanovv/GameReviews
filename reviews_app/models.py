from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=GameReview.Status.PUBLISHED)


class GameReview(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг')
    content = models.TextField(blank=True, verbose_name='Обзор')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время последнего обновления')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.PUBLISHED, verbose_name='Статус')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категории')
    tags = models.ManyToManyField('TagReview', blank=True, related_name='tags', verbose_name='Теги')
    price = models.OneToOneField('Price', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Цена')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None, blank=True, null=True, verbose_name='Фото')

    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='reviews', null=True, default=None)

    objects = models.Manager()
    published = PublishedManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_base = slugify(self.title)
            slug = slug_base
            counter = 1
            while GameReview.objects.filter(slug=slug).exists():
                slug = f"{slug_base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'обзор на игру'
        verbose_name_plural = 'Обзоры на игры'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('review', kwargs={'review_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagReview(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return str(self.tag)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Price(models.Model):
    full_price = models.IntegerField(null=True)
    sale = models.IntegerField(null=True)

    def __str__(self):
        return str(self.full_price)


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')