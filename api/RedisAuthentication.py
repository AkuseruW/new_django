from django.utils.translation import gettext as _
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api import redis_connect
from django.contrib.auth import get_user_model
import json


class RedisTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        user_data = redis_connect.get(key)
        if user_data:
            user_dict = json.loads(user_data)
            user_obj = get_user_model()()

            for key_name, value in user_dict.items():
                setattr(user_obj, key_name, value)

            return user_obj, key
        raise AuthenticationFailed(_('Invalid token.'))