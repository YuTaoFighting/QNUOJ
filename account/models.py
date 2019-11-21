from django.db import models


class User(models.Model):
    username = models.TextField(unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_disabled = models.BooleanField(default=False)

    class Meta:
        db_table = "user"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ac_problems = models.TextField(default='', blank=True)
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


class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)
    users = models.ManyToManyField(User)

    class Meta:
        db_table = "role"


class Permission(models.Model):
    name = models.CharField(max_length=64, unique=True)
    roles = models.ManyToManyField(Role)

    class Meta:
        db_table = "permission"
