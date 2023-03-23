from django.urls import path
from .views import RegistrationView, TokenView

urlpatterns = [
    path('signup/', RegistrationView.as_view(), name='signup'),
    path('token/', TokenView.as_view(), name='token'),
]