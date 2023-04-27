from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorAndModeratorOrReadOnly(BasePermission):
    """Права доступа для автора комментария/отзыва и для модератора."""

    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user or request.user.is_moderator
                or request.method in SAFE_METHODS
                )

