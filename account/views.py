import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend

# from rest_framework_extensions.cache import mixins

from rest_framework import viewsets, mixins, status, exceptions
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from account.auth import UserAuth
from account.models import UserProfile, User
from utils.exceptions import UserDisabledException, UserDoesNotExistException, TokenInvalidException
from utils.paginations import CommonPagination
from account.permissions import UserPermission, UsersPermission
from account.serializers import UserProfileSerializer, UserSerializer, UserRegisterSerializer, EditUserSerializer, \
    RankListSerializer, UserProfilesSerializer

HTTP_ACTION_LOGIN = 'login'
HTTP_ACTION_REGISTER = 'register'
HTTP_ACTION_LOGOUT = 'logout'


def perform_save(serializer):
    data = serializer.data
    if data['password'] and len(data['password']) > 0:
        data['password'] = make_password(data['password'])
    return data


class RankListAPIView(generics.ListAPIView):
    authentication_classes = (UserAuth,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('user__username',)
    pagination_class = CommonPagination
    serializer_class = RankListSerializer
    queryset = UserProfile.objects.filter(user__is_disabled=False).exclude(
        user__permissions__name='topic maker').order_by("-rating", "-ac_total", "user__username")


class UserProfilesAPIView(generics.ListAPIView):
    authentication_classes = (UserAuth,)
    serializer_class = UserProfilesSerializer
    queryset = UserProfile.objects.all()


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    authentication_classes = (UserAuth,)
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class UsersAPIView(generics.ListAPIView):
    authentication_classes = (UserAuth,)
    permission_classes = (UsersPermission,)
    pagination_class = CommonPagination
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        action = request.query_params.get('action')

        if action == HTTP_ACTION_REGISTER:
            serializer = UserRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                user = User.objects.create(**perform_save(serializer))
                UserProfile.objects.create(user=user)
                return Response({
                    'detail': 'register success',
                    'data': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'permissions': [permission.name for permission in user.permissions.all()],
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
                    'username': [
                        '用户名: %s  已存在。' % serializer.data.get('username')
                    ],
                }, status=status.HTTP_400_BAD_REQUEST)
            except TypeError:
                raise exceptions.ParseError

        elif action == HTTP_ACTION_LOGIN:
            username = request.data.get('username')
            password = request.data.get('password')
            try:
                user = User.objects.get(username=username)
                if user.is_disabled:
                    raise UserDisabledException
                if check_password(password, user.password):
                    token = uuid.uuid4().hex
                    cache.set(token, user.id, 60 * 60 * 2)
                    data = {
                        'detail': 'login success',
                        'token': token,
                        'data': {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'permissions': [permission.name for permission in user.permissions.all()],
                        }
                    }
                    return Response(data=data, status=status.HTTP_200_OK)
                else:
                    raise exceptions.AuthenticationFailed
            except User.DoesNotExist:
                raise UserDoesNotExistException
        elif action == HTTP_ACTION_LOGOUT:
            token = request.query_params.get('token')
            u_id = cache.get(token)
            try:
                User.objects.get(pk=u_id)
                cache.delete(token)
                return Response({
                    'detail': '退出登录成功。'
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                raise TokenInvalidException
        else:
            raise exceptions.ParseError


class UserAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (UserAuth,)
    permission_classes = (UserPermission,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        if isinstance(request.user, User) and \
                (request.user.permissions.filter(name='update user').exists() or
                 request.user.id == int(kwargs['pk'])):
            serializer = EditUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                user = User.objects.get(pk=kwargs['pk'])
                data = perform_save(serializer)
                if data['password'] and len(data['password']) > 0:
                    user.password = data['password']
                if data['email'] and len(data['email']) > 0:
                    user.email = data['email']
                user.is_disabled = data['is_disabled']
                user.save()
                res = {
                    'id': user.id,
                    'username': user.username,
                    'is_disabled': user.is_disabled
                }
                if data['password'] and len(data['password']) > 0:
                    res['password'] = serializer.data['password']
                if data['email'] and len(data['email']) > 0:
                    res['email'] = user.email
                return Response({
                    'msg': 'update success',
                    'data': res
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                raise exceptions.NotFound
            except Exception:
                raise exceptions.ParseError
        else:
            raise exceptions.PermissionDenied
