from datetime import datetime

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Title, Review, User


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для категорий."""

    class Meta:
        fields = '__all__'
        model = Category


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для комментариев."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('review',)
        model = Comment


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер для названий произведений."""
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title
    
    def validate(self, data):
        if data['year'] > datetime.now().year:
            raise serializers.ValidationError(
                'Год создания не может быть больше текущего!')
        return data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзыва."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['username', 'title']
            )
        ]


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""

    class Meta:
        fields = '__all__'
        model = User
