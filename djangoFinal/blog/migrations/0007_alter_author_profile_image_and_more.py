# Generated by Django 4.1.2 on 2022-12-17 22:42

from django.db import migrations, models
import djangoFinal.blog.validators


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_author_profile_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='profile_image',
            field=models.ImageField(default='none.png', upload_to='images', validators=[djangoFinal.blog.validators.validate_image_size]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(default='none.png', upload_to='images', validators=[djangoFinal.blog.validators.validate_image_size]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='none.png', upload_to='images', validators=[djangoFinal.blog.validators.validate_image_size]),
        ),
    ]
