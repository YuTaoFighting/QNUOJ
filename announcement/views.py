from rest_framework import generics

from account.auth import UserAuth
from announcement.models import Announcement
from utils.paginations import CommonPagination
from announcement.serializers import AnnouncementSerializer, AnnouncementsSerializer


class AnnouncementsAPIView(generics.ListCreateAPIView):
    authentication_classes = (UserAuth,)
    pagination_class = CommonPagination
    queryset = Announcement.objects.filter(is_visible=True)
    serializer_class = AnnouncementsSerializer


class AnnouncementAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (UserAuth,)
    queryset = Announcement.objects.filter(is_visible=True)
    serializer_class = AnnouncementSerializer
