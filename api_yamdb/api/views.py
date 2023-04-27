from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, views, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from api.filters import TitleFilter
from .mixins import ModelMixinSet
from .models import Category, Genre, Title, User, Review
from .permissions import IsAdminUserOrReadOnly
from .utils import create_conf_code
from .serializers import (CategorySerializer, GenreSerializer, 
                          TitleReadSerializer, TitleWriteSerializer,
                          MyselfSerializer, SignUpSerializer, TokenSerializer,
                          UserSerializer
                        )


class GenreViewSet(ModelMixinSet):
    permission_classes = [IsAdminUserOrReadOnly, ]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class CategoryViewSet(ModelMixinSet):
    permission_classes = [IsAdminUserOrReadOnly, ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitleViewSet(ModelMixinSet):
    permission_classes = [IsAdminUserOrReadOnly, ]
    # queryset = Title.objects.all().annotate(Avg('reviews__score'))
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer

        return TitleWriteSerializer




class ReviewViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)



class APISignUp(views.APIView):
    """ View-класс для регистрации пользователя."""

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            user = User.objects.create(
                username=username,
                email=email,
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
    permission_classes = [IsAdminUser]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )


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
