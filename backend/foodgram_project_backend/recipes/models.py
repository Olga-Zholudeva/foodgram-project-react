from django.core.validators import MinValueValidator
from django.db import models

from users.models import User

COUNT_ING = int(1)


class Tag(models.Model):
    name = models.CharField(
        'Период приема пищи',
        max_length=50,
        unique=True
    )
    color = models.CharField(
        'Цвет кнопки',
        max_length=50,
        unique=True
    )
    slug = models.SlugField(
        'Часть url-адреса',
        unique=True
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=120,
        db_index=True
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=10
    )

    def __str__(self):
        return self.name


class Recept(models.Model):
    name = models.CharField(
        'Название блюда',
        max_length=120
    )
    author = models.ForeignKey(
        User,
        related_name='recepts',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        'Изображение блюда',
        upload_to='recipes/images/'
        )
    text = models.TextField(
        'Как приготовить блюдо'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recepts',
        through='ReceptTabel'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recepts'
    )
    cooking_time = models.IntegerField(
        'Время приготовления блюда'
    )
    pub_date = models.DateTimeField(
        'Дата добавления рецепта',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class ReceptTabel(models.Model):
    recept = models.ForeignKey(
        Recept,
        on_delete=models.CASCADE,
        related_name='recept'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient'
    )
    amount = models.IntegerField(
        'Количество ингредиента',
        validators=(
            MinValueValidator(
                COUNT_ING,
                message='Количество менее 1'
            ),
        )
    )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recept = models.ForeignKey(
        Recept,
        on_delete=models.CASCADE,
        related_name='favorite'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recept'],
                name='unique_user_recept'
                )
            ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    recept = models.ForeignKey(
        Recept,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recept'],
                name='unique_user_recept_shopping_cart'
                )
            ]
