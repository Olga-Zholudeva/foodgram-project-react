from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import Recept
from users.models import Follow, User


class GetUserSerializer(UserSerializer):
    """Сериализатор для получения данных о пользователе."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        model = User

    def get_is_subscribed(self, object):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user, author=object
        ).exists()


class CreateUserSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password')
        model = User


class GetFollowUserSerializer(serializers.ModelSerializer):
    """ Выдаем информацию о подписках пользователя."""

    id = serializers.ReadOnlyField(source="author.id")
    username = serializers.ReadOnlyField(source="author.username")
    email = serializers.ReadOnlyField(source="author.email")
    first_name = serializers.ReadOnlyField(source="author.first_name")
    last_name = serializers.ReadOnlyField(source="author.last_name")
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        model = Follow

    def get_recipes(self, id):
        recipes = Recept.objects.filter(author=id.author)
        return ShortReceptSerializer(recipes, many=True).data

    def get_recipes_count(self, id):
        return Recept.objects.filter(author=id.author).count()

    def get_is_subscribed(self, id):
        return Follow.objects.filter(
            user=id.user, author=id.author
        ).exists()


class ShortReceptSerializer(serializers.ModelSerializer):
    """Сериализатор для сокращенных данных рецепта."""

    class Meta:
        model = Recept
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
