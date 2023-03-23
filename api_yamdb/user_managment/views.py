from django.core.mail import send_mail
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import AuthSerializer, UsersSerializer
from .permisions import IsAdmin, IsOwnerIReadOnly
from reviews.models import User

class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = User.objects.filter(username=request.data.get('username')).first()
        serializer = AuthSerializer(data=request.data)
        
        if not user:
            if serializer.is_valid():
                user = serializer.save()

                confirmation_code = '123456' #Сделать рандомный ключ
                email_message = f'Your confirmation code is: {confirmation_code}'
                send_mail(
                    'Confirmation Code',
                    email_message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

                return Response(data=request.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        confirmation_code = '123456' #Сделать рандомный ключ
        email_message = f'Your confirmation code is: {confirmation_code}'
        send_mail(
            'Confirmation Code',
            email_message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
                )
        return Response(data=request.data, status=status.HTTP_200_OK)

class TokenView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        if username:

            user = User.objects.filter(username=username).first()

            if not user:
                return Response({'error':'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            if confirmation_code == '123456': #Сделать рандомный ключ

                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(token, status=status.HTTP_200_OK)

            return Response({'error':'Invalid confirmation code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
from rest_framework.pagination import PageNumberPagination

class UserCreateView(APIView):

    permission_classes = [IsAdmin]
    http_method_names = ['get', 'head', 'post']

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        email = request.data.get('email', None)
        existing_user = User.objects.filter(email=email).exists()

        if serializer.is_valid() and not existing_user:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
