from django.db import models


class Permission(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        db_table = "permission"


class User(models.Model):
    username = models.TextField(unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_disabled = models.BooleanField(default=False)
    permissions = models.ManyToManyField(Permission)

    class Meta:
        db_table = "user"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    desc = models.TextField(null=True, blank=True)
    ac_problems = models.TextField(default='', blank=True)
    ac_total = models.PositiveIntegerField(default=0)
    real_name = models.TextField(null=True)
    avatar = models.TextField(null=True)
    blog = models.URLField(null=True)
    github = models.TextField(null=True)
    school = models.TextField(null=True)
    major = models.TextField(null=True)
    rating = models.FloatField(default=1500.0)

    def add_accepted_problem(self, problem):
        ac_problems = self.ac_problems.strip().split(' ')
        if str(problem.id) in ac_problems:
            pass
        else:
            self.ac_problems = models.F('ac_problems') + str(problem.id) + ' '
            self.save()

    class Meta:
        db_table = "user_profile"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest_id = models.IntegerField()
    contest_title = models.TextField()
    contest_begin_time = models.DateTimeField()
    rating = models.FloatField(default=1500.0)
    change = models.FloatField(default=0.0)

    class Meta:
        db_table = "rating_change"
        unique_together = (("user", "contest_id"),)
