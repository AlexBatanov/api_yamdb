from rest_framework import serializers, status

from reviews.models import User

class AuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email']
    
    def validate(self, data):
        if 3 < len(data['username']) > 150:
            raise serializers.ValidationError(
                'username пользователя должно содержать не менее 3 и не более 254 символов.'
                )

        if 3 < len(data['email']) > 254:
            raise serializers.ValidationError(
                'email электронной почты должен содержать не менее 5 и не более 254 символов.'
                )
        
        email = User.objects.filter(email=data['email']).exists()
        username = User.objects.filter(username=data['username']).exists()

        if email and not username:
            raise serializers.ValidationError(
                'Такой email уже существует.'
                )
        
        if not email and username:
            raise serializers.ValidationError(
                'Такой username уже существует.'
                )
        
        return data
    
class UsersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'
    
    def validate(self, data):
        if 3 < len(data['username']) > 150:
            raise serializers.ValidationError(
                'username пользователя должно содержать не менее 3 и не более 254 символов.'
                )
        if data.get('first_name') and 3 < len(data['first_name']) > 150:
            raise serializers.ValidationError(
                'first_name пользователя должно содержать не менее 3 и не более 254 символов.'
                )
        if data.get('last_name') and 3 < len(data['last_name']) > 150:
            raise serializers.ValidationError(
                'last_name пользователя должно содержать не менее 3 и не более 254 символов.'
                )

        if 3 < len(data['email']) > 254:
            raise serializers.ValidationError(
                'email электронной почты должен содержать не менее 5 и не более 254 символов.'
                )
        return data
