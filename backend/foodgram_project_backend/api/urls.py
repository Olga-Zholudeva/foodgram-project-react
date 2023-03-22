from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from api.views import DownloadSoppingCartViewSet, FavoriteViewSet, FollowViewSet, IngredientViewSet, ReceptViewSet, ShoppingCartViewSet, TagViewSet

router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', ReceptViewSet, basename='recipes')
#router.register(r'^users/subscriptions', FollowViewSet)
#router.register(r'^users/(?P<id>\d+)/subscribe', FollowViewSet)

urlpatterns = [
    path('recipes/download_shopping_cart/', DownloadSoppingCartViewSet.as_view({'get': 'download'}),
        name='download_shopping_cart'),
    re_path(r'recipes/(?P<id>\d+)/shopping_cart/', ShoppingCartViewSet.as_view({'post': 'create', 'delete': 'delete'})),
    re_path(r'recipes/(?P<id>\d+)/favorite/', FavoriteViewSet.as_view({'post': 'create', 'delete': 'delete'})),
    path('users/subscriptions/', FollowViewSet.as_view({'get': 'list'}),
        name='subscriptions'),
    re_path(r'users/(?P<id>\d+)/subscribe/', FollowViewSet.as_view({'post': 'create', 'delete': 'delete'}),
        name='subscribe'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.authtoken'))
]