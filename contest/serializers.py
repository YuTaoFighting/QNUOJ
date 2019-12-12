import datetime

from rest_framework import serializers

from account.serializers import UserSerializer
from contest.models import Contest


class ContestsSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    created_by = UserSerializer(read_only=True)
    registrant_total = serializers.SerializerMethodField()

    class Meta:
        model = Contest
        fields = ['id', 'title', 'rule_type', 'begin_time', 'end_time', 'status', 'registrant_total', 'created_by']

    def get_registrant_total(self, obj):
        return obj.registrants.count()

    def get_status(self, obj):
        if obj.begin_time >= datetime.datetime.now():
            return 'Pending'
        elif obj.end_time <= datetime.datetime.now():
            return 'Ended'
        return 'Running'


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = '__all__'
