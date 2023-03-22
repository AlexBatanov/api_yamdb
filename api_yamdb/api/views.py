from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from user_managment.permisions import IsOwnerIReadOnly, IsModerator, IsAdmin
from .serializers import CommentSerializer, ReviewSerializer
from reviews.models import Review, Title


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerIReadOnly, IsModerator, IsAdmin,)

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
    permission_classes = (IsOwnerIReadOnly, IsModerator, IsAdmin,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)
