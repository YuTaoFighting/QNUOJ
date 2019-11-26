from rest_framework import generics

from announcement.models import Announcement
from utils.paginations import CommonPagination
from announcement.serializers import AnnouncementSerializer


class AnnouncementsAPIView(generics.ListCreateAPIView):
    pagination_class = CommonPagination
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer


class AnnouncementAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
