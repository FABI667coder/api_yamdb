from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, views, viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User
from .filters import TitleFilter
from .mixins import ModelMixinSet, TitleModelMixinSet
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, MyselfSerializer, ReviewSerializer,
                          SignUpSerializer, TitleReadSerializer,
                          TitleWriteSerializer, TokenSerializer,
                          UserSerializer)
from .utils import create_conf_code
from .permissions import IsAdmin, IsAdminOrReadOnly, IsOwnerOrAdminOrModerator
from .pagination import PagePagination


class APIToken(views.APIView):
    """View-класс для получения токена."""

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']
            user = get_object_or_404(User, username=username)
            if confirmation_code == user.confirmation_code:
                token = str(AccessToken.for_user(user))
                return Response(
                    {'token': token},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для добавление/удаления пользователей администратором."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ('username',)
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = PagePagination


class UserProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    http_method_names = ['get', 'patch', 'delete']


class APIMyself(views.APIView):
    """
    View-класс для просмотра пользователем
     собственных данных и изменять их.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_object_or_404(User, username=self.request.user)
        serializer = MyselfSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = get_object_or_404(User, username=self.request.user)
        serializer = MyselfSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class GenreViewSet(ModelMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    pagination_class = PagePagination
    search_fields = ['name', ]
    lookup_field = 'slug'


class CategoryViewSet(ModelMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    pagination_class = PagePagination
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitleViewSet(TitleModelMixinSet):
    queryset = Title.objects.all().annotate(Avg('reviews__score'))
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    pagination_class = PagePagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsOwnerOrAdminOrModerator]

    def get_id(self):
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_id().reviews.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            title=self.get_id())


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsOwnerOrAdminOrModerator]
    pagination_class = PagePagination

    def get_id(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_id().comments.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            review=self.get_id()
        )


class APISignUp(views.APIView):
    """ View-класс для регистрации пользователя."""

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            try:
                user, created = User.objects.get_or_create(
                    username=username,
                    email=email,
                )
            except IntegrityError:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            confirmation_code = create_conf_code()
            user.confirmation_code = confirmation_code
            user.save()
            send_mail(
                'Confirmation code',
                confirmation_code,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
