from rest_framework import generics

from remoteoj.models import RemoteOJ
from remoteoj.serializers import RemoteOJSerializer


class RemoteOJAPIView(generics.ListAPIView):
    queryset = RemoteOJ.objects.filter(is_active=True)
    serializer_class = RemoteOJSerializer
