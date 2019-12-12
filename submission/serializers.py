from rest_framework import serializers

from problem.serializers import SubmissionProblemSerializer
from submission.models import Submission


class SubmissionsSerializer(serializers.ModelSerializer):
    problem = SubmissionProblemSerializer()
    code_len = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ['id', 'problem', 'result', 'score',
                  'use_time_ms', 'use_memory_bytes',
                  'language', 'code_len', 'user_id',
                  'username', 'create_time']

    def get_code_len(self, obj):
        return len(obj.code)


# class SubmissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Submission
#         fields = ['id', 'result', 'score', 'user_time_ms',
#                   'use_memory_bytes', '']


class ContestSubmissionsSerializer(serializers.ModelSerializer):
    problem = SubmissionProblemSerializer()
    _id = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ['id', '_id', 'problem', 'result', 'score',
                  'use_time_ms', 'use_memory_bytes',
                  'language', 'username', 'create_time']

    def get__id(self, obj):
        contest = obj.contest
        return Submission.objects.filter(contest=contest).filter(create_time__lt=obj.create_time).count() + 1


class ProblemSubmitSerializer(serializers.Serializer):
    problem_id = serializers.IntegerField()
    contest_id = serializers.IntegerField(default=None)
    code = serializers.CharField()
    language = serializers.CharField()
    user_id = serializers.IntegerField()
    username = serializers.CharField()
