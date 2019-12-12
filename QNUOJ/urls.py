"""QNUOJ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from announcement.views import AnnouncementAPIView, AnnouncementsAPIView
from account.views import UsersAPIView, UserAPIView, UserProfilesAPIView, UserProfileAPIView, RankListAPIView
from contest.views import ContestsAPIView, ContestAPIView
from problem.views import ProblemsAPIView, ProblemAPIView, Problem_idAPIView
from remoteoj.views import RemoteOJAPIView
from submission.views import SubmissionsAPIView, SubmissionAPIView
from utils.views import FriendLinksAPIView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/$', UsersAPIView.as_view()),
    url(r'^users/(?P<pk>\d+)/$', UserAPIView.as_view()),
    url(r'^userprofiles/$', UserProfilesAPIView.as_view()),
    url(r'^userprofiles/(?P<pk>\d+)/$', UserProfileAPIView.as_view()),
    url(r'^announcements/$', AnnouncementsAPIView.as_view()),
    url(r'^announcements/(?P<pk>\d+)/$', AnnouncementAPIView.as_view()),
    url(r'^ranklist/$', RankListAPIView.as_view()),
    url(r'^problems/$', ProblemsAPIView.as_view()),
    url(r'^problems/(?P<pk>\d+)/$', ProblemAPIView.as_view()),
    url(r'^problems/(?P<id>[a-zA-Z]+-\d+)/$', Problem_idAPIView.as_view()),
    url(r'^contests/$', ContestsAPIView.as_view()),
    url(r'^contests/(?P<pk>\d+)/$', ContestAPIView.as_view()),
    url(r'^submissions/$', SubmissionsAPIView.as_view()),
    url(r'^submissions/(?P<pk>\d+)/$', SubmissionAPIView.as_view()),
    url(r'^general/activeojs/$', RemoteOJAPIView.as_view()),
    url(r'^general/friendlinks/$', FriendLinksAPIView.as_view()),
]
