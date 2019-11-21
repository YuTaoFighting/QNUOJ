from django.db import models

from account.models import User
from contest.models import Contest


class ProblemTag(models.Model):
    name = models.CharField(max_length=128, unique=True)
    bg_color = models.CharField(max_length=32, null=True, blank=True)
    font_color = models.CharField(max_length=32, null=True, blank=True)
    type = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = "problem_tag"


class Problem(models.Model):
    _id = models.TextField(db_index=True)
    oj = models.CharField(max_length=32)
    contest = models.ForeignKey(Contest, null=True, on_delete=models.CASCADE)

    # for contest problem
    is_public = models.BooleanField(default=False)

    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    input_desc = models.TextField(null=True, blank=True)
    output_desc = models.TextField(null=True, blank=True)

    samples = models.TextField(null=True, blank=True)

    hint = models.TextField(null=True, blank=True)
    source = models.TextField(null=True, blank=True)

    languages = models.TextField(default="['C', 'C++', 'Java', 'Python2', 'Python3']")

    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    #  ms
    time_limit = models.IntegerField(default=1000)
    #  MB
    memory_limit = models.IntegerField(default=512)

    is_spj = models.BooleanField(default=False)
    is_spj_compile_ok = models.BooleanField(default=False)

    is_visible = models.BooleanField(default=True)

    tags = models.ManyToManyField(ProblemTag)

    score = models.IntegerField(default=100)

    submit_total = models.IntegerField(default=0)
    ac_total = models.IntegerField(default=0)

    # {JudgeStatus.ACCEPTED: 3, JudgeStaus.WRONG_ANSWER: 11}, the number means count
    statistic_info = models.TextField(default='{}')

    def add_submit_total(self):
        self.submit_total = models.F("submit_total") + 1
        self.save(update_fields=["submit_total"])

    def add_ac_total(self):
        self.ac_total = models.F("ac_total") + 1
        self.save(update_fields=["ac_total"])

    class Meta:
        db_table = "problem"
        unique_together = (("_id", "contest"),)
        ordering = ("create_time",)
