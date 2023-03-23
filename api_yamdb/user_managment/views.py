from django.core.mail import send_mail
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework import generics

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
from rest_framework import pagination

class UserList(generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = pagination.LimitOffsetPagination


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdmin]

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def get(self, request, *args, **kwargs):
        if kwargs.get('username') == 'me':
            instance = User.objects.get(username=request.user.username)
        else:
            instance = User.objects.get(username=kwargs.get('username'))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        print(request.data)
        if kwargs.get('username') == 'me':
            # instance = User.objects.get(username=request.user.username)
            serializer = self.get_serializer(request.data)
            return Response(serializer.data)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# class UserViewSet(APIView):

#     permission_classes = [IsAdmin]
#     http_method_names = ['get', 'head', 'post']

#     def get(self, request, format=None):
#         users = User.objects.all()
#         serializer = UsersSerializer(users, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = UsersSerializer(data=request.data)
#         email = request.data.get('email', None)
#         existing_user = User.objects.filter(email=email).exists()

#         if serializer.is_valid() and not existing_user:
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserViewSet(viewsets.ModelViewSet):

#     permission_classes = [permissions.AllowAny]
#     serializer_class = UsersSerializer
#     queryset = User.objects.all()

#     def list(self, request):
#         serializer = self.get_serializer(self.queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = self.get_serializer(data=request.data)
#         email = request.data.get('email', None)
#         existing_user = self.queryset.filter(email=email).exists()

#         if serializer.is_valid() and not existing_user:
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk=None):
#         user = self.get_object()
#         serializer = self.get_serializer(user)
#         return Response(serializer.data)
    
    # def update(self, request, pk=None):
    #     user = self.get_object()
    #     serializer = self.get_serializer(user, data=request.data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def partial_update(self, request, pk=None):
    #     user = self.get_object()
    #     serializer = self.get_serializer(user, data=request.data, partial=True)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request, pk=None):
    #     user = self.get_object()
    #     user.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)