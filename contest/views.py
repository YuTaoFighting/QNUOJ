from django.db.models.functions import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, exceptions, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin, RetrieveCacheResponseMixin

from account.auth import UserAuth
from account.models import User
from account.serializers import RegistrantsSerializer
from contest.models import Contest
from contest.serializers import ContestsSerializer, ContestSerializer
from problem.models import Problem
from problem.serializers import ContestProblemsSerializer
from submission.models import Submission
from submission.serializers import ContestSubmissionsSerializer
from utils.exceptions import ContestDoesNotExistException, ContestIsPendingException, ContestIsEndedException
from utils.paginations import CommonPagination


class ContestsAPIView(ListCacheResponseMixin, generics.ListCreateAPIView):
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('rule_type',)
    search_fields = ('title',)
    authentication_classes = (UserAuth,)
    pagination_class = CommonPagination
    queryset = Contest.objects.all()
    serializer_class = ContestsSerializer

    def post(self, request, *args, **kwargs):
        action = request.query_params.get('action')
        if action == 'register':
            contest_id = request.data.get('contest_id')
            try:
                contest = Contest.objects.get(pk=contest_id)
                if isinstance(request.user, User):
                    if not contest.registrants.filter(pk=request.user.id).exists():
                        if contest.begin_time > datetime.datetime.now():
                            contest.add_registrant(request.user)
                        elif contest.begin_time <= datetime.datetime.now() <= contest.end_time:
                            raise ContestIsEndedException(detail='比赛已经开始，无法报名!')
                        elif contest.end_time < datetime.datetime.now():
                            raise ContestIsEndedException(detail='比赛已经结束，无法报名!')
                else:
                    raise exceptions.NotAuthenticated
                serializer = ContestSerializer(contest)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Contest.DoesNotExist:
                raise ContestDoesNotExistException
        elif action == 'create':
            return self.create(request, *args, **kwargs)
        else:
            raise exceptions.ParseError

    def get_queryset(self):
        index = self.request.query_params.get('index')
        status = self.request.query_params.get('status')

        if index == 'true':
            return Contest.objects.exclude(end_time__lte=datetime.datetime.now())
        else:
            if status == 'Pending':
                return Contest.objects.filter(begin_time__gte=datetime.datetime.now())
            elif status == 'Running':
                return Contest.objects.filter(begin_time__lte=datetime.datetime.now()). \
                    filter(end_time__gte=datetime.datetime.now())
            elif status == 'Ended':
                return Contest.objects.filter(end_time__lte=datetime.datetime.now())
        return self.queryset.all()

    # def get_serializer_class(self):
    #     print(self.request._request.method)
    #     return self.serializer_class


class ContestAPIView(RetrieveCacheResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (UserAuth,)
    queryset = Contest.objects.all()
    pagination_class = CommonPagination
    serializer_class = ContestSerializer

    def get(self, request, *args, **kwargs):
        resource = request.query_params.get('resource')
        if resource == 'registrants':
            try:
                registrants = Contest.objects.get(pk=kwargs['pk']).registrants
                serializer = RegistrantsSerializer(registrants, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Contest.DoesNotExist:
                raise ContestDoesNotExistException
        elif resource == 'problems':
            try:
                contest = Contest.objects.get(pk=kwargs['pk'])
                if contest.begin_time > datetime.datetime.now():
                    raise ContestIsPendingException(detail='比赛还未开始， 无法查看题目!')
                problems = Problem.objects.filter(contest=contest).order_by('_id')
                serializer = ContestProblemsSerializer(problems, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Contest.DoesNotExist:
                raise ContestDoesNotExistException
        elif resource == 'submissions':
            try:
                contest = Contest.objects.get(pk=kwargs['pk'])
                if contest.begin_time > datetime.datetime.now():
                    raise ContestIsPendingException(detail='比赛还未开始， 无法查看提交记录!')
                mine = request.query_params.get('mine')
                submissions = Submission.objects.all()
                if mine == 'true':
                    submissions = submissions.filter(user_id=request.user.id)
                submissions = submissions.filter(contest=contest).order_by('-create_time')
                page = self.paginate_queryset(submissions)
                serializer = ContestSubmissionsSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            except Contest.DoesNotExist:
                raise ContestDoesNotExistException
        else:
            return self.retrieve(request, *args, **kwargs)
