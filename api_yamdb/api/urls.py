from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ReviewViewSet, CommentsViewSet, APIMyself, APISignUp, APIToken, UserViewSet

router_v1 = DefaultRouter()

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
    path('v1/auth/signup/', APISignUp.as_view()),
    path('v1/auth/token/', APIToken.as_view()),
    path('v1/users/me/', APIMyself.as_view()),
    path('v1/', include(router_v1.urls)),
    ]