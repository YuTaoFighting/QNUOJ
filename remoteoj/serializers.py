from rest_framework import serializers

from remoteoj.models import RemoteOJ


class RemoteOJSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    class Meta:
        model = RemoteOJ
        fields = ['text', 'value']

    def get_text(self, obj):
        return obj.name

    def get_value(self, obj):
        return obj.name
