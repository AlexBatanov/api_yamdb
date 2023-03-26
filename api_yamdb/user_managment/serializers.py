import re

from rest_framework import serializers, status
from django.shortcuts import get_object_or_404

from reviews.models import User

class AuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email']
    
    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('"me" - нельзя использовать для usermname')
        
        return data
    
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']

    def validate_username(self, username):
        pattern = r'^[a-zA-Z0-9.@_\\+\\-\\|]'
        if bool(re.match(pattern, username)):
            return username
        raise serializers.ValidationError('недопустимые символы')
    
    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(f'{username} занято')
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(f'{email} занято')

        if email and len(email) > 254:
            raise serializers.ValidationError('длина email должна быть меньше 254 символов')
        
        for field in ('username', 'first_name', 'last_name'):
            field = data.get(field)
            if field and 1 < len(field) > 150:
                raise serializers.ValidationError(f'{field} не должен привышать 150 символов')
            
        return data
    
    # def update(self, instance, validated_data):
    #     print(3)
    #     return super().update(instance, **validated_data)
