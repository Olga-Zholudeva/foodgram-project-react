from django.contrib import admin
from django.contrib.auth import get_user_model
from recipes.models import (Favorite, Ingredient, Recept, ReceptTabel,
                            ShoppingCart, Tag)
from users.models import Follow

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'password',
    )
    list_filter = (
        'email',
        'username',
    )


class ReceptIngredientsInline(admin.TabularInline):
    model = ReceptTabel
    min_num = 1
    extra = 1


@admin.register(Recept)
class ReceptAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
    )
    list_filter = (
        'author',
        'name',
        'tags'
    )
    readonly_fields = ('in_favorites',)
    inlines = (ReceptIngredientsInline,)

    def in_favorites(self, object):
        return object.favorite.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)


@admin.register(ReceptTabel)
class ReceptTabelAdmin(admin.ModelAdmin):
    list_display = (
        'recept',
        'ingredient',
        'amount',
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug'
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recept',
    )


@admin.register(ShoppingCart)
class ShoppingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recept',
    )
