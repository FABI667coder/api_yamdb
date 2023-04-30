from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (APIMyself, APISignUp, APIToken, CategoryViewSet,
                    CommentsViewSet, GenreViewSet, ReviewViewSet, TitleViewSet,
                    UserProfile, UserViewSet)

app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
urlpatterns = [
    path(
        'v1/auth/signup/',
        APISignUp.as_view(),
        name='sign_up'
    ),
    path(
        'v1/auth/token/',
        APIToken.as_view(),
        name='token'
    ),
    path(
        'v1/users/me/',
        APIMyself.as_view(),
        name='myself'
    ),
    path(
        'v1/users/<str:username>/',
        UserProfile.as_view(),
        name='profile'
    ),
    path('v1/', include(router_v1.urls)),
]
