from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from api.filters import TitleFilter
from .mixins import ModelMixinSet
from .models import Category, Genre, Title
from .permissions import IsAdminUserOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer, 
                          TitleReadSerializer, TitleWriteSerializer,
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

