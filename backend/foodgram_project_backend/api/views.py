from api.filters import IngredientFilter
from api.permissions import AuthorOrReadOnly
from api.serializers import (CreateReceptSerializer, GetReceptSerializer,
                             IngredientSerializer, TagSerializer)
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, Recept, ReceptTabel,
                            ShoppingCart, Tag)
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from users.models import Follow
from users.serializers import GetFollowUserSerializer, ShortReceptSerializer

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Обрабатываем запросы к модели тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Обрабатываем запросы к модели ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class ReceptViewSet(viewsets.ModelViewSet):
    """Обрабатываем запросы к модели рецептов."""
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [AuthorOrReadOnly, ]

    def get_queryset(self):
        queryset = Recept.objects.all()
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart'
        )
        is_favorited = self.request.query_params.get('is_favorited')
        author = self.request.query_params.get('author')
        tags = self.request.query_params.getlist('tags')
        if is_in_shopping_cart == '1':
            queryset = queryset.filter(
                shopping_cart__user=self.request.user
            )
        if is_favorited == '1':
            queryset = queryset.filter(
                favorite__user=self.request.user
            )
        if author:
            queryset = queryset.filter(
                author_id=author
            )
        if tags:
            queryset = queryset.filter(
                tags__slug__in=tags
            ).distinct()
        else:
            return queryset

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GetReceptSerializer
        return CreateReceptSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    """Подписка на авторов."""
    serializer_class = GetFollowUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def create(self, request, id):
        author = get_object_or_404(User, id=id)
        if Follow.objects.filter(user=request.user, author=author):
            return Response(
                {'errors': 'Вы уже подписаны на данного автора'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.user == author:
            return Response(
                {'errors': 'Вы пытаетесь подписаться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Follow.objects.create(
            user=request.user,
            author=author
        )
        serializer = GetFollowUserSerializer(
            get_object_or_404(
                Follow, user=request.user, author=author
            ),
            many=False
        )
        return Response(
            data=serializer.data, status=status.HTTP_201_CREATED
        )

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        follow = Follow.objects.filter(
            user=request.user, author=author
        )
        if not follow.exists():
            return Response(
                {'errors': 'Вы не подписаны на данного автора'},
                status=status.HTTP_400_BAD_REQUEST
            )
        follow.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class FavoriteViewSet(viewsets.ViewSet):
    """Добавление рецепта в избранное."""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def create(self, request, id):
        recept = get_object_or_404(Recept, id=id)
        if Favorite.objects.filter(user=request.user, recept=recept):
            return Response(
                {'errors': 'Данный рецепт уже есть в избранных'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Favorite.objects.create(
            user=request.user,
            recept=recept
        )
        serializer = ShortReceptSerializer(
            recept,
            many=False
        )
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        recept = get_object_or_404(Recept, id=id)
        favorite = Favorite.objects.filter(
            user=request.user, recept=recept
        )
        if not favorite.exists():
            return Response(
                {'errors': 'Вы не подписаны на данный рецепт'},
                status=status.HTTP_400_BAD_REQUEST
            )
        favorite.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class ShoppingCartViewSet(viewsets.ViewSet):
    """Добавление/удаление рецепта в список покупок."""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def create(self, request, id):
        recept = get_object_or_404(Recept, id=id)
        if ShoppingCart.objects.filter(user=request.user, recept=recept):
            return Response(
                {'errors': 'Данный рецепт уже есть в писке покупок'},
                status=status.HTTP_400_BAD_REQUEST
            )
        ShoppingCart.objects.create(
            user=request.user,
            recept=recept
        )
        serializer = ShortReceptSerializer(
            recept,
            many=False
        )
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        recept = get_object_or_404(Recept, id=id)
        shoppingcart = ShoppingCart.objects.filter(
            user=request.user, recept=recept
        )
        if not shoppingcart.exists():
            return Response(
                {'errors': 'Данного рецепта нет в спике покупок'},
                status=status.HTTP_400_BAD_REQUEST
            )
        shoppingcart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadSoppingCartViewSet(viewsets.ViewSet):
    """Выгрузка файла со списком покупок."""
    permission_classes = [permissions.IsAuthenticated]

    def download(self, request):
        shopping_cart = ShoppingCart.objects.filter(user=request.user)
        recepts = [item.recept.id for item in shopping_cart]
        shoping_list = ReceptTabel.objects.filter(
            recept__in=recepts
        ).values(
            'ingredient'
        ).annotate(
            amount=Sum('amount')
        )
        shoping_list_text = 'Список покупок:\n\n'
        for item in shoping_list:
            ingredient = Ingredient.objects.get(pk=item['ingredient'])
            amount = item['amount']
            shoping_list_text += (
                f'{ingredient.name} ({ingredient.measurement_unit})'
                f'- {amount}\n'
            )

        response = HttpResponse(shoping_list_text, content_type="text/plain")
        response['Content-Disposition'] = (
            'attachment; filename=shoping_list.txt'
        )
        return response
