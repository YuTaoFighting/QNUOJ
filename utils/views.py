from rest_framework import generics

from utils.models import FriendLink
from utils.serializers import FriendLinksSerializer


class FriendLinksAPIView(generics.ListCreateAPIView):
    queryset = FriendLink.objects.all()
    serializer_class = FriendLinksSerializer
