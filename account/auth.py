from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication

from account.models import User


class UserAuth(BaseAuthentication):

    def authenticate(self, request):
        token = request.query_params.get('token')
        try:
            u_id = cache.get(token)
            user = User.objects.get(pk=u_id)
            cache.set(token, u_id, 60 * 60 * 2)
            return user, token
        except:
            return None
