from django.db import models
from django.utils.timezone import now

from account.models import User
from contest.models import Contest
from problem.models import Problem


class JudgeStatus(object):
    COMPILE_ERROR = -2
    WRONG_ANSWER = -1
    ACCEPTED = 0
    PRESENTATION_ERROR = 1
    MEMORY_LIMIT_EXCEEDED = 2
    TIME_LIMIT_EXCEEDED = 3
    OUTPUT_LIMIT_EXCEEDED = 4
    RUNTIME_ERROR = 5
    SYSTEM_ERROR = 6
    JUDGING = 7
    QUEUING = 8


class Submission(models.Model):
    contest = models.ForeignKey(Contest, null=True, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField(db_index=True)
    username = models.TextField()
    code = models.TextField()
    score = models.IntegerField(default=0)
    result = models.IntegerField(db_index=True, default=JudgeStatus.QUEUING)
    info = models.TextField(null=True, blank=True)
    language = models.TextField()
    shared = models.BooleanField(default=False)

    # ms
    use_time_ms = models.IntegerField(default=0)
    # MB
    use_memory_m_bytes = models.IntegerField(default=0)

    ip = models.TextField(null=True)

    def check_user_permission(self, user, check_share=True):
        if self.user_id == user.id or self.problem.created_by_id == user.id:
            return True
        for role in user.role_set:
            for permission in role.permission_set:
                if permission.id == 1:
                    return True
        if check_share:
            if self.contest and self.contest.end_time > now():
                return False
            if self.shared:
                return True
        return False

    class Meta:
        db_table = "submission"
        ordering = ("-create_time",)

    def __str__(self):
        return self.id
