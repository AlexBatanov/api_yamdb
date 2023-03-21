import random

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer


CONFIRMATION_CODE = str(random.randint(100000, 999999))

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def registration_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # генерация кода с отправкой письма
        email_message = f'Ваш код подтверждения: {CONFIRMATION_CODE}'
        send_mail(
            'Код подтверждения',
            email_message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        return Response({'успешно':'Код подтверждения отправлен на почту'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def token_view(request):
    username = request.data['username']
    confirmation_code = request.data['confirmation_code']

    # Получаем пользователя по имени
    user = User.objects.filter(username=username).first()

    # Проверяем код
    if user and confirmation_code == CONFIRMATION_CODE:
        # Генерируем токен
        refresh = RefreshToken.for_user(user)
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(token, status=status.HTTP_200_OK)

    return Response({'error':'Invalid confirmation code'}, status=status.HTTP_400_BAD_REQUEST)
