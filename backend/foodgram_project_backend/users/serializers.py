from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recept
from rest_framework import serializers
from users.models import Follow

User = get_user_model()


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
        if not request or request.user.is_anonymous:
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
        try:
            recept_limit = int(
                self.context.get('request').query_params['recipes_limit']
            )
            queryset = Recept.objects.filter(author=id.author)[:recept_limit]
        except Exception:
            queryset = Recept.objects.filter(author=id.author)
        serializer = ShortReceptSerializer(
            queryset, read_only=True, many=True
        )
        return serializer.data

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
