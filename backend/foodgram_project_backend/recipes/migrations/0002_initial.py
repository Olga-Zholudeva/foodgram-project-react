# Generated by Django 3.2.18 on 2023-03-19 13:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='recept',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recepts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recept',
            name='ingredients',
            field=models.ManyToManyField(related_name='recepts', through='recipes.ReceptTabel', to='recipes.Ingredient'),
        ),
        migrations.AddField(
            model_name='recept',
            name='tags',
            field=models.ManyToManyField(related_name='recepts', to='recipes.Tag'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='recept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='recipes.recept'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='recept',
            constraint=models.UniqueConstraint(fields=('name', 'author'), name='unique_recept'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recept'), name='unique_user_recept'),
        ),
    ]