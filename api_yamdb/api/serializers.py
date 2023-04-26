from django.conf import settings
from rest_framework import serializers

from reviews.models import Review, Comments


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
