from rest_framework import serializers

from utils.models import FriendLink


class FriendLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendLink
        fields = '__all__'
