from rest_framework.permissions import BasePermission

from account.models import User


class SubmissionPermission(BasePermission):

    def has_permission(self, request, view):

        if request.method == 'POST':
            action = request.query_params.get('action')
            if action == 'rejudge':
                return isinstance(request.user, User) and \
                       request.user.permissions.filter(name='rejudge submissions').exists()
            else:
                return isinstance(request.user, User)
        else:
            return True
