import uuid

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from api import redis_connect


class RedisTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        user_data = redis_connect.get(key)
        if user_data:
            try:
                if isinstance(user_data, bytes):
                    user_data = user_data.decode("utf-8")

                user_id = uuid.UUID(user_data)
                user_obj = get_user_model().objects.get(id=user_id)
                return user_obj, key
            except ValueError:
                raise AuthenticationFailed(_("Invalid user ID."))
            except get_user_model().DoesNotExist:
                raise AuthenticationFailed(_("User not found."))
        raise AuthenticationFailed(_("Invalid token."))
