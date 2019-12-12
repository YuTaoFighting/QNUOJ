import json

from rest_framework import serializers

from problem.models import Problem, ProblemTag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemTag
        fields = '__all__'


class ProblemsSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Problem
        fields = ['id', '_id', 'title', 'tags', 'ac_total', 'submit_total']


class ContestProblemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', '_id', 'title', 'ac_total', 'submit_total']


class ProblemSerializer(serializers.ModelSerializer):
    languages = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = '__all__'

    def get_created_by(self, obj):
        return obj.created_by.username

    def get_languages(self, obj):
        return json.loads(obj.languages)


class SubmissionProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', '_id', 'title']
