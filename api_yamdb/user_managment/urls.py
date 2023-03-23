from django.urls import path
from .views import RegistrationView, TokenView, UserCreateView

urlpatterns = [
    path('signup/', RegistrationView.as_view(), name='signup'),
    # path('token/', TokenView.as_view(), name='token'),
    # path('users/', UserCreateView.as_view(), name='users'),
]