import re

from rest_framework import serializers, status
from django.shortcuts import get_object_or_404

from reviews.models import User

class AuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email']
    
    # def validate(self, data):
    #     print('vhod')
    #     if 3 < len(data['username']) > 150:
    #         raise serializers.ValidationError(
    #             'username пользователя должно содержать не менее 3 и не более 254 символов.'
    #             )

    #     if 3 < len(data['email']) > 254:
    #         raise serializers.ValidationError(
    #             'email электронной почты должен содержать не менее 5 и не более 254 символов.'
    #             )

    #     email = User.objects.filter(email=data['email']).first()
    #     user = User.objects.filter(username=data['username']).first()

    #     if email and not user:
    #         raise serializers.ValidationError(
    #             'Такой email уже существует.'
    #             )
        
    #     if not email and user:
    #         raise serializers.ValidationError(
    #             'Такой username уже существует.'
    #             )
        
    #     if user and user.email != data['email']:
    #         raise serializers.ValidationError(
    #             'не верный email.'
    #             )
        
    #     return data
    
class UsersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']

    def validate_username(self, username):
        pattern = r'^[a-zA-Z0-9.@_\\+\\-\\|]'
        if bool(re.match(pattern, username)):
            return username
        raise serializers.ValidationError('недопустимые символы')

    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)
    
    # # def validate(self, data):
    #     print('validating')
    #     print(data.get('username'))
    #     user = User.objects.filter(username=data.get('username')).first()
    #     print(user)
    #     print('validating user')
    #     if user:
    #         raise serializers.ValidationError(
    #             'Такой username уже существует.'
    #             )
    #     email = User.objects.filter(email=data.get('email')).exists()
    #     if email:
    #         raise serializers.ValidationError(
    #             'Такой email уже существует.'
    #             )
    #     if 3 < len(data['username']) > 150:
    #         raise serializers.ValidationError(
    #             'username пользователя должно содержать не менее 3 и не более 254 символов.'
    #             )
    #     if data.get('first_name') and 3 < len(data['first_name']) > 150:
    #         raise serializers.ValidationError(
    #             'first_name пользователя должно содержать не менее 3 и не более 254 символов.'
    #             )
    #     if data.get('last_name') and 3 < len(data['last_name']) > 150:
    #         raise serializers.ValidationError(
    #             'last_name пользователя должно содержать не менее 3 и не более 254 символов.'
    #             )

    #     if 3 < len(data['email']) > 254:
    #         raise serializers.ValidationError(
    #             'email электронной почты должен содержать не менее 5 и не более 254 символов.'
    #             )
    #     return data
