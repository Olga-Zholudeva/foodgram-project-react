from django.contrib import admin

from recipes.models import (Favorite, Ingredient, Recept, ReceptTabel,
                            ShoppingCart, Tag)
from users.models import Follow, User


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

    def in_favorites(self, object):
        return object.favorite.count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recept, ReceptAdmin)
admin.site.register(ReceptTabel)
admin.site.register(Follow)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
admin.site.register(User, UserAdmin)
