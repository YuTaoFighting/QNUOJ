from django.db import models


class RemoteOJ(models.Model):
    name = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = "remote_oj"


class RemoteOJAccount(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=128)
    remote_oj = models.ForeignKey(RemoteOJ, on_delete=models.CASCADE)

    class Meta:
        db_table = "remote_account"
