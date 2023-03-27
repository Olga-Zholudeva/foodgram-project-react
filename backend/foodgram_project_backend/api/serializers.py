import base64

from django.core.files.base import ContentFile
from recipes.models import (Favorite, Ingredient, Recept, ReceptTabel,
                            ShoppingCart, Tag)
from rest_framework import serializers
from users.serializers import GetUserSerializer


class TagSerializer(serializers.ModelSerializer):
    """ Сериализатор для получения данных из модели с тегами."""

    class Meta:
        fields = (
            'id', 'name', 'color', 'slug',
        )
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    """ Сериализатор для получения данных из модели с ингрединтами."""

    class Meta:
        fields = '__all__'
        model = Ingredient


class Base64ImageField(serializers.ImageField):
    """ Сериализатор для кодирования картинок."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class ReceptTabelSerializer(serializers.ModelSerializer):
    """Сериализатор для создания записи в промежуточной таблице ингредиентов"""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        fields = (
            'id', 'amount'
        )
        model = ReceptTabel


class CreateReceptSerializer(serializers.ModelSerializer):
    """ Сериализатор для создания и изменения рецепта."""

    ingredients = ReceptTabelSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    image = Base64ImageField(required=True)

    class Meta:
        fields = (
            'name', 'image', 'text', 'ingredients', 'tags', 'cooking_time'
        )
        model = Recept

    def recepttabel_objects_create(self, ingredients, recept):
        for ingredient in ingredients:
            ReceptTabel.objects.create(
                recept=recept,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recept = Recept.objects.create(**validated_data)
        recept.tags.set(tags)
        self.recepttabel_objects_create(ingredients, recept)
        return recept

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        ReceptTabel.objects.filter(recept=instance).delete()
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        if tags:
            instance.tags.clear()
        if ingredients:
            instance.ingredients.clear()
        self.ingredient_tag_in_instance(instance, ingredients, tags)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return GetReceptSerializer(instance).data


class GetReceptTabelSerializer(serializers.ModelSerializer):
    """Получаем данные для чтения из промежуточной модели ингредиентов."""

    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.ReadOnlyField()

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = ReceptTabel


class GetReceptSerializer(serializers.ModelSerializer):
    """ Сериализатор для get запросов к рецептам."""

    ingredients = GetReceptTabelSerializer(many=True, source='recept')
    tags = TagSerializer(many=True, read_only=True)
    author = GetUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name', 'image',
            'text',
            'cooking_time',
        )
        model = Recept

    def get_is_favorited(self, object):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user, recept=object
        ).exists()

    def get_is_in_shopping_cart(self, object):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recept=object
        ).exists()
