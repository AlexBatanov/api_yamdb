from django.http import Http404
from rest_framework import permissions, status, viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import AuthSerializer, UsersSerializer
from .permisions import IsAdmin
from reviews.models import User
from .helper import send_massege


PATTERN = r'^[\\w.@+-]+\\z'

class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = User.objects.filter(username=request.data.get('username')).first()
        email = User.objects.filter(email=request.data.get('email')).first()
        serializer = AuthSerializer(data=request.data)

        if not user and not email:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            send_massege(user)

            return Response(data=request.data, status=status.HTTP_200_OK)

        if user and user.email == request.data.get('email'):
            send_massege(user)
            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response({'error: username и email должны быть уникальны'}, status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        if username:
            user = User.objects.filter(username=username).first()

            if not user:
                return Response({'error':'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            if confirmation_code == user.key:
                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(token, status=status.HTTP_200_OK)

            return Response({'error':'Invalid confirmation code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get_object(self):
        name = self.request.parser_context['kwargs']['pk']

        if name == 'me':
            instance = User.objects.get(username=self.request.user.username)
        else:
            try:
                instance = User.objects.get(username=name)
            except Exception:
                raise Http404

        return instance
    
    def partial_update(self, request, *args, **kwargs):
        
        if kwargs.get('pk') == 'me' and request.data.get('role'):
            return Response({'error':'нельзя изменять роль'}, status=status.HTTP_400_BAD_REQUEST)

        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):

        if kwargs.get('pk') == 'me':
            return Response({'error':'просите админа'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        return super().destroy(request, *args, **kwargs)

    # def destroy(self, request, *args, **kwargs):

    #     if self.request.parser_context['kwargs']['pk'] == 'me':
    #         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    #     instance = self.get_object()
    #     self.perform_destroy(User.objects.get(username=instance['username']))

    #     return Response(status=status.HTTP_204_NO_CONTENT)
