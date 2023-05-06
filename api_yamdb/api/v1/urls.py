from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, CreateUserViewSet,
                    GenreViewSet, GetTokenViewSet, ReviewViewSet, TitleViewSet,
                    UserViewSet)

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename='comments'
)

auth = [
    path(
        'signup/',
        CreateUserViewSet.as_view({'post': 'create'}),
        name='signup'
    ),
    path(
        'token/',
        GetTokenViewSet.as_view({'post': 'create'}),
        name='token'
    ),
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include(auth)),
]
