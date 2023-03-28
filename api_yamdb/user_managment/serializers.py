import re

from rest_framework import serializers
from reviews.models import User
from rest_framework.validators import UniqueValidator

from .helper import get_users


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError(
                'длина email должна быть меньше 254 символов')
        return value
        
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('username не может быть me')

        if not re.match(r'[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                'поле username должно содержать только латинские буквы и цифры')

        if len(value) > 150:
            raise serializers.ValidationError(
                'длина username должна быть меньше 150 символов')
        return value


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']

    def validate(self, data):
        email = data.get('email')

        if any(get_users(data)):
            raise serializers.ValidationError(
                'поля username и email должны быть  уникальными')

        if email and len(email) > 254:
            raise serializers.ValidationError(
                'длина email должна быть меньше 254 символов')

        for field in ('username', 'first_name', 'last_name'):
            field = data.get(field)
            if field and 1 < len(field) > 150:
                raise serializers.ValidationError(
                    f'{field} не должен привышать 150 символов')

        return data
