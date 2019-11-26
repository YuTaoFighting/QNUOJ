import uuid

from django.core.cache import cache
from django.db import IntegrityError
from rest_framework import viewsets, mixins, status, exceptions

from rest_framework import generics
from rest_framework.response import Response

from account.auth import UserAuth
from account.models import UserProfile, User
from utils.paginations import CommonPagination
from account.permissions import UserPermission
from account.serializers import UserProfileSerializer, UserSerializer, UserRegisterSerializer

HTTP_ACTION_LOGIN = 'login'
HTTP_ACTION_REGISTER = 'register'


class UserProfilesAPIView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token', None)
        if token:
            try:
                u_id = cache.get(token)
                user = User.objects.get(pk=u_id)
                return Response({
                    'id': user.id,
                    'username': user.username,
                    'roles': [permission.name for permission in user.permissions.all()]
                }, status=status.HTTP_200_OK)
            except:
                raise exceptions.ParseError
        else:
            return self.list(request, *args, **kwargs)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class UsersAPIView(generics.ListAPIView):
    authentication_classes = (UserAuth,)
    permission_classes = (UserPermission,)
    pagination_class = CommonPagination
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        action = request.query_params.get('action')

        if action == HTTP_ACTION_REGISTER:
            serializer = UserRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                user = User.objects.create(**serializer.data)
                UserProfile.objects.create(user=user)
                return Response({
                    'msg': 'register success',
                    'data': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'real_name': user.userprofile.real_name,
                        'blog': user.userprofile.blog,
                        'github': user.userprofile.github,
                        'school': user.userprofile.school,
                        'major': user.userprofile.major,
                        'rating': user.userprofile.rating
                    }
                }, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({
                    'detail': '用户名: %s  已存在' % serializer.data.get('username'),
                }, status=status.HTTP_400_BAD_REQUEST)
            except TypeError:
                raise exceptions.ParseError

        elif action == HTTP_ACTION_LOGIN:
            username = request.data.get('username')
            password = request.data.get('password')
            try:
                user = User.objects.get(username=username)
                if user.password == password:
                    token = uuid.uuid4().hex
                    cache.set(token, user.id, 60 * 60 * 2)
                    data = {
                        'msg': 'login success',
                        'token': token,
                        'data': {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'real_name': user.userprofile.real_name,
                            'blog': user.userprofile.blog,
                            'github': user.userprofile.github,
                            'school': user.userprofile.school,
                            'major': user.userprofile.major,
                            'rating': user.userprofile.rating
                        }
                    }
                    return Response(data=data, status=status.HTTP_200_OK)
                else:
                    raise exceptions.AuthenticationFailed
            except User.DoesNotExist:
                raise exceptions.NotFound
        else:
            raise exceptions.ParseError


class UserAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (UserAuth,)
    permission_classes = (UserPermission,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
