from rest_framework import mixins, viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.viewsets import GenericViewSet


class TitleModelMixinSet(CreateModelMixin, ListModelMixin,
                         DestroyModelMixin, UpdateModelMixin,
                         GenericViewSet, RetrieveModelMixin
                         ):
    pass


class ModelMixinSet(CreateModelMixin,
                    ListModelMixin,
                    DestroyModelMixin,
                    GenericViewSet):
    pass


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass
