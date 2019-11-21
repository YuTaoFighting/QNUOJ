from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from account.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()

    serializer_class = UserSerializer


# class GroupViewSet(viewsets.ModelViewSet):
#
#     queryset = Group.objects.all()
#
#     serializer_class = GroupSerializer


class UserView(APIView):

    def post(self, request):

        data = JSONParser().parse(request)
        print(data)
        return JsonResponse({'msg': 'ok'})

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(UserView, self).dispatch(*args, **kwargs)
