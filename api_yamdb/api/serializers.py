from django.conf import settings
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Genre, Title, User, Review, Comments


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        model = Category


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title



class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    def validate_score(self, value):
        if settings.MIN_SCORE > value > settings.MAX_SCORE:
            raise serializers.ValidationError(
                (f'Оценка должна быть от {settings.MIN_SCORE}'
                 f'до {settings.MAX_SCORE}!')
            )
        return value

    class Meta:
        model = Review
        fields = ('id', 'author', 'title', 'text', 'score', 'pub_date')


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        model = Comments
        fields = ('id', 'author', 'review', 'text', 'pub_date')
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class MyselfSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Username already exists',
        )]
    )
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Username already exists',
        )]
    )

    class Meta:
        fields = ('email', 'username',)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError("U can't use username 'me'")
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    confirmation_code = serializers.CharField(
        required=True,
    )

    class Meta:
        fields = ('username', 'confirmation_code',)

