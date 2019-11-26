from rest_framework.permissions import BasePermission
from utils.utils import has_permission

from account.models import User, Permission


class UserPermission(BasePermission):

    def has_permission(self, request, view):

        if request.method == 'GET':
            if isinstance(request.user, User):
                # permission = Permission.objects.get(pk=1)
                # print(request.user.role_set)
                return True
            return False
        elif request.method == 'POST':
            return True

        else:
            return True
