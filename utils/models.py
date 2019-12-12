from django.db import models


class FriendLink(models.Model):
    url = models.URLField(max_length=128)
    name = models.CharField(max_length=64)

    class Meta:
        db_table = "friend_link"
