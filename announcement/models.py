from django.db import models

from account.models import User


class Announcement(models.Model):
    title = models.TextField()

    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update_time = models.DateTimeField(auto_now=True)
    is_visible = models.BooleanField(default=True)

    class Meta:
        db_table = "announcement"
        ordering = ("-last_update_time",)
