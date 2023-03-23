from rest_framework import serializers

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
        if 3 < len(data['first_name']) > 150:
            raise serializers.ValidationError(
                'first_name пользователя должно содержать не менее 3 и не более 254 символов.'
                )
        if 3 < len(data['last_name']) > 150:
            raise serializers.ValidationError(
                'last_name пользователя должно содержать не менее 3 и не более 254 символов.'
                )

        if 3 < len(data['email']) > 254:
            raise serializers.ValidationError(
                'email электронной почты должен содержать не менее 5 и не более 254 символов.'
                )
        return data