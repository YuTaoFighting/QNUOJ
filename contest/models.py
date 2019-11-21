from django.db import models

from account.models import User, Permission


class ContestRuleType(object):
    ACM = "ACM"
    OI = "OI"
    LanQiaoBei = "LanQiaoBei"


class Contest(models.Model):
    title = models.TextField()
    description = models.TextField()
    real_time_rank = models.BooleanField(default=True)
    rule_type = models.CharField(max_length=12)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)
    allowed_ips = models.TextField(default='', null=True, blank=True)
    enter_permission = models.TextField(default=f'allow_contest:{id}')
    rank_permission = models.TextField(default=f'allow_look_rank_at_any_time:{id}')

    @property
    def is_allow(self, user):
        for role in user.role_set:
            for permission in role.permission_set:
                if permission.name == self.enter_permission:
                    return True
        return False

    @property
    def is_allow_look_rank_at_any_time(self, user):
        for role in user.role_set:
            for permission in role.permission_set:
                if permission.name == self.rank_permission:
                    return True
        return False

    class Meta:
        db_table = "contest"
        ordering = ("-begin_time",)


class AbstractContestRank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    submission_number = models.IntegerField(default=0)

    class Meta:
        abstract = True


class ACMContestRank(AbstractContestRank):
    ac_number = models.IntegerField(default=0)
    total_time = models.IntegerField(default=0)
    submission_info = models.TextField(default='{}')

    class Meta:
        db_table = "acm_contest_rank"
        unique_together = (("user", "contest"),)


class OILanQiaoBeiContestRank(AbstractContestRank):
    total_score = models.IntegerField(default=0)
    submission_info = models.TextField(default='{}')

    class Meta:
        db_table = "oi_lqb_contest_rank"
        unique_together = (("user", "contest"),)


class ContestAnnouncement(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "contest_announcement"
        ordering = ("-create_time",)
