import os

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from django.contrib.auth.models import CustomUser
from django.urls import reverse

from pathlib import Path

from djangoFinal import settings
from taggit.managers import TaggableManager
from django.core import validators
from djangoFinal.blog.validators import validate_only_alphabet, validate_image_size

from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import AbstractUser

# from ckeditor_uploader.fields import RichTextUploadingField

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MIN_LEN_USERNAME = 2
MAX_LEN_USERNAME = 15


from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime

# Create your models here.
class CustomUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to='images',
        default='images/none.png',
        validators=[
            validate_image_size
        ]
    )

    def __str__(self):
        return f"{self.id}"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    profile_image = models.ImageField(
        upload_to='images',
        default='images/none.png',
        validators=[
            validate_image_size
        ]
    )

    email_confirmed = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profilе"


class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.CharField(max_length=100, default="")

    profile_image = models.ImageField(
        upload_to='images',
        default='images/none.png',
        validators=[
            validate_image_size
        ]
    )

    def __str__(self):
        return f"Author: {self.user.first_name} {self.user.last_name}"


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset() \
            .filter(status='published')


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category_articles',
                       kwargs={'slug': self.slug})


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')

    body = RichTextField(config_name='awesome_ckeditor')
    widget = CKEditorWidget(config_name='awesome_ckeditor')

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Custom manager.
    tags = TaggableManager()

    post_image = models.ImageField(
        upload_to='images',
        default='images/none.png',
        validators=[
            validate_image_size
        ]
    )

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by on {}'.format(self.post)


class Testimonial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_testimonial')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    job_position = models.CharField(
        default="",
        max_length=255,
        null=True,
        blank=True,
    )


class NewsletterEmail(models.Model):
    email = models.EmailField()

    def __str__(self):
        return f"email: {self.email}"


# TODO Get authenticated user when commenting

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    company = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.email


class AboutUsContent(models.Model):
    about_body = RichTextField(config_name='awesome_ckeditor')


class TCContent(models.Model):
    tc_body = RichTextField(config_name='awesome_ckeditor')
