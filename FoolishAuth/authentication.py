# -*- coding: utf-8 -*-
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from .settings import FOOLISH_AUTH_USER_SAVED


class FoolishAuthentication(BaseAuthentication):
    """
    只是简单的认可请求头中携带的用户信息，然后创建一个不保存的零时用户。
    此APP只能用于带有认证功能的API网关背后，用于简化系统内部的用户认证。
    """

    def authenticate(self, request):
        username = request.META.get('HTTP_FOOLISH_AUTH')
        if username is None:
            return None

        UserModel = get_user_model()

        if FOOLISH_AUTH_USER_SAVED:
            try:
                user = UserModel.objects.get(**{UserModel.USERNAME_FIELD: username})
            except ObjectDoesNotExist:
                return None
        else:
            user = UserModel(**{UserModel.USERNAME_FIELD: username})

        return user, username
