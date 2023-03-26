import random
import re

from django.conf import settings
from django.core.mail import send_mail

CONFIRMATION_CODE = random.randint(1000, 9999)


def is_valid_username(username):
    pattern = r'^[a-zA-Z0-9.@_\\+\\-\\|]'
    print(username)
    print(re.match(pattern, username))
    return bool(re.match(pattern, username))


def send_massege(user):
    """
    Оптправляет на почту сообщение с генерированым ключом.
    присваивает ключ к юзеру
    """
    email_message = f'Your confirmation code is: {CONFIRMATION_CODE}'
    send_mail(
        'Confirmation Code',
        email_message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
    user.key = CONFIRMATION_CODE
    user.save()
