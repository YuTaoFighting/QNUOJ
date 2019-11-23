from rest_framework.routers import DefaultRouter

from account.views import UserProfileViewSet, UserViewSet

router = DefaultRouter()

router.register(r'userprofile', UserProfileViewSet)
router.register(r'users', UserViewSet)
