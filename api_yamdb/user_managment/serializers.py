from rest_framework import serializers
from reviews.models import User

from .helper import get_users


class AuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email']

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                '"me" - нельзя использовать для usermname')

        return data


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
