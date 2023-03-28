from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .helpers import send_massege, get_users
from .serializers import AuthSerializer, UsersSerializer
from api.permissions import IsAdmin
from reviews.models import User


class RegistrationView(APIView):
    """
    Регистрация пользователя с прверкой username и email на уникальность,
    в случае успеха создает юзера и оправляет секретный ключ на почту.

    Если пользователь уже существует в системе, то происходит повторная
    отправка секретного ключа на почту.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):

        serializer = AuthSerializer(data=request.data)
        user_filter_name, user_filter_email = get_users(request.data)

        if not user_filter_name and not user_filter_email:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            send_massege(user)

            return Response(data=request.data, status=status.HTTP_200_OK)

        if (user_filter_name
                and user_filter_name.email == request.data.get('email')):
            send_massege(user_filter_name)

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(
            {'error: username и email должны быть уникальны'},
            status=status.HTTP_400_BAD_REQUEST
        )


class TokenView(APIView):
    """
    Выдает токен для авторизации пользователя.

    проверяет существование юзера и секретного ключа.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):

        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        if username:
            user = User.objects.filter(username=username).first()

            if not user:
                return Response(
                    {'error': 'пользоваетель не найден'},
                    status=status.HTTP_404_NOT_FOUND
                )

            if confirmation_code == user.key:
                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(token, status=status.HTTP_200_OK)

            return Response(
                {'error': 'не верный ключ'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    Реализация CRUD для пользователей.

    переопределены методы получения, обновления и удаления,
    для работы со своим профилем исходя из требований.
    """

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_object(self):
        name = self.request.parser_context['kwargs']['pk']

        if name == 'me':
            instance = get_object_or_404(
                User,
                username=self.request.user.username
            )
        else:
            instance = get_object_or_404(User, username=name)

        return instance

    def partial_update(self, request, *args, **kwargs):

        if kwargs.get('pk') == 'me' and request.data.get('role'):
            return Response(
                {'error': 'нельзя изменять роль'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):

        if kwargs.get('pk') == 'me':
            return Response(
                {'error': 'просите админа'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        return super().destroy(request, *args, **kwargs)
