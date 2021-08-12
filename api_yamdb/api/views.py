from django.contrib.auth import get_user_model
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.filters import SearchFilter

from .serializers import CustomUserSerializer, ReviewSerializer, CommentSerializer 
from .permissions import IsSuperUser, IsAdminUserOrReadOnly, CustomPermission
from reviews.models import Title, Genre, Category, Review, Comment
from .serializers import (TitleReadSerializer, GenreSerializer,
                          CategorySerializer, TitleCreateSerializer)
from .filters import Filter

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsSuperUser,)
    lookup_field = 'username'


class CustomViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=(Avg('reviews__score')))
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = Filter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleCreateSerializer


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_backends = (SearchFilter,)
    search_fields = ('slug', 'name')
    lookup_field = 'slug'


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_backends = (SearchFilter,)
    search_fields = ('slug', 'name')
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [CustomPermission]
    ordering = ('-pub_date',)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [CustomPermission]

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user)