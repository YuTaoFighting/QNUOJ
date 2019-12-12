import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from account.auth import UserAuth
from judge.tasks import judge
from submission.models import Submission
from submission.permissions import SubmissionPermission
from submission.serializers import SubmissionsSerializer, ProblemSubmitSerializer
from rest_framework import exceptions

from utils.exceptions import SubmissionDoesNotExistException, SubmissionUserDoesNotSelfException
from utils.paginations import CommonPagination

logger = logging.getLogger('log')


class SubmissionsAPIView(generics.ListCreateAPIView):
    authentication_classes = (UserAuth,)
    permission_classes = (SubmissionPermission,)
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filter_fields = ('language', 'result',)
    search_fields = ('problem___id', 'problem__title', 'username',)
    queryset = Submission.objects.all()
    pagination_class = CommonPagination
    serializer_class = SubmissionsSerializer

    def post(self, request, *args, **kwargs):
        action = request.query_params.get('action')
        if action == 'rejudge':
            submission_id = request.query_params.get('id')
            try:
                submission_id = int(submission_id)
                submission = Submission.objects.get(pk=submission_id)
                judge.send(submission.id)
                logger.info('rejudge submission: %d' % submission.id)
                return Response({
                    'detail': 'Rejudge Success!'
                }, status=status.HTTP_200_OK)
            except Submission.DoesNotExist:
                raise SubmissionDoesNotExistException
            except:
                raise exceptions.ParseError
        else:
            return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = ProblemSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            if serializer.data.get('user_id') != request.user.id:
                raise SubmissionUserDoesNotSelfException
            submission = Submission.objects.create(**serializer.data)
            judge.send(submission.id)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'id': submission.id,
            }, status=status.HTTP_201_CREATED, headers=headers)
        except SubmissionUserDoesNotSelfException:
            raise SubmissionUserDoesNotSelfException
        except:
            raise exceptions.ParseError


class SubmissionAPIView(generics.RetrieveAPIView):
    authentication_classes = (UserAuth,)
    # permission_classes = ()
    queryset = Submission.objects.all()
    serializer_class = SubmissionsSerializer
