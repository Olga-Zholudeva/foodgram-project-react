from django.contrib import admin


from recipes.models import Favorite, Ingredient, Recept, ReceptTabel, Tag
from users.models import User, Follow



admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recept)
admin.site.register(ReceptTabel)
admin.site.register(Follow)
admin.site.register(Favorite)

