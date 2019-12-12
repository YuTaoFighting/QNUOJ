from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, exceptions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from account.auth import UserAuth
from problem.models import Problem
from problem.serializers import ProblemsSerializer, ProblemSerializer
from utils.exceptions import ProblemDoesNotExistException
from utils.paginations import CommonPagination


class ProblemsAPIView(generics.ListAPIView):
    authentication_classes = (UserAuth,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('tags__name',)
    search_fields = ('_id', 'title')
    ordering_fields = ('_id', 'title', 'ac_total', 'submit_total')
    queryset = Problem.objects.filter(is_visible=True)
    serializer_class = ProblemsSerializer
    pagination_class = CommonPagination


class ProblemAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (UserAuth,)
    queryset = Problem.objects.filter(is_visible=True)
    serializer_class = ProblemSerializer


class Problem_idAPIView(generics.RetrieveAPIView):
    authentication_classes = (UserAuth,)
    queryset = Problem.objects.filter(is_visible=True)
    serializer_class = ProblemSerializer

    def retrieve(self, request, *args, **kwargs):
        _id = kwargs['id']
        try:
            problem = Problem.objects.get(_id=_id)
            serializer = ProblemSerializer(problem)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Problem.DoesNotExist:
            raise ProblemDoesNotExistException
