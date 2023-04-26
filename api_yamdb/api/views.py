from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, views, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import User
from .utils import create_conf_code
from .serializers import (MyselfSerializer, SignUpSerializer, TokenSerializer,
                          UserSerializer)


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
