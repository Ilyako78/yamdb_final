# Generated by Django 3.2 on 2023-02-03 17:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Категория')),
                ('slug', models.SlugField(unique=True, validators=[django.core.validators.RegexValidator('^[-a-zA-Z0-9_]+$')], verbose_name='Адрес категории')),
            ],
            options={
                'verbose_name': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Жанр')),
                ('slug', models.SlugField(unique=True, validators=[django.core.validators.RegexValidator('^[-a-zA-Z0-9_]+$')], verbose_name='Адрес жанра')),
            ],
            options={
                'verbose_name': 'Жанры',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('year', models.IntegerField(db_index=True, verbose_name='Год')),
                ('rating', models.IntegerField(null=True, verbose_name='Рейтинг поста')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(related_name='titles', to='reviews.Genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
                'ordering': ('name',),
            },
        ),
    ]
