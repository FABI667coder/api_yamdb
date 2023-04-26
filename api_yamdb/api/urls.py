from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import APIMyself, APISignUp, APIToken, UserViewSet

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', APISignUp.as_view()),
    path('v1/auth/token/', APIToken.as_view()),
    path('v1/users/me/', APIMyself.as_view()),
    path('v1/', include(router_v1.urls)),
]
