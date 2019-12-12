from rest_framework.permissions import BasePermission

from account.models import User, Permission


class UserPermission(BasePermission):

    def has_permission(self, request, view):

        if request.method == 'GET':
            return isinstance(request.user, User)
        elif request.method == 'DELETE':
            return isinstance(request.user, User) and \
                   request.user.permissions.filter(name='delete user').exists()
        else:
            return True


class UsersPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return isinstance(request.user, User) and \
                   request.user.permissions.filter(name='retrieve user').exists()
        else:
            return True
