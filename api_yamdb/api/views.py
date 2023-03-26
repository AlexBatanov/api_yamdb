# https://docs.djangoproject.com/en/4.1/topics/db/aggregation/
# https://docs.djangoproject.com/en/4.1/ref/models/querysets/#django.db.models.query.QuerySet.annotate

from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

from .filters import TitleFilter
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializerForRead,
    TitleSerializerForChange,
    CommentSerializer,
    ReviewSerializer
)
from reviews.models import Category, Genre, Title, Review
from user_managment.permisions import IsAdminOrReadOnly, IsOwnerIReadOnly, IsModerator, IsAdmin


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerIReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerIReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""
    queryset = Title.objects.all().annotate(
        rating = Avg('reviews__score')
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializerForRead
        return TitleSerializerForChange
