from rest_framework import serializers
from django import forms
from rest_framework.utils import model_meta

from account.models import User, UserProfile, Permission


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    tfa_code = serializers.CharField(required=False, allow_blank=True)


class UsernameOrEmailCheckSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(min_length=6)
    email = serializers.CharField(max_length=64)


class UserChangeEmailSerializer(serializers.Serializer):
    password = serializers.CharField()
    new_email = serializers.CharField(max_length=64)
    tfa_code = serializers.CharField(required=False, allow_blank=True)


class GenerateUserSerializer(serializers.Serializer):
    prefix = serializers.CharField(max_length=16, allow_blank=True)
    suffix = serializers.CharField(max_length=16, allow_blank=True)
    number_from = serializers.IntegerField()
    number_to = serializers.IntegerField()
    password_length = serializers.IntegerField(max_value=16, default=8)


# class ImportUserSerializer(serializers.Serializer):
#     users = serializers.ListField(
#         child=serializers.DictField()
#     )


class UserAdminSerializer(serializers.ModelSerializer):
    real_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'real_name', 'create_time', 'is_disabled']

    def get_real_name(self, obj):
        return obj.userprofile.realname


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'permissions', 'create_time', 'is_disabled']

    def get_permissions(self, obj):
        return [permission.name for permission in obj.permissions.all()]


class UserProfilesSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email']

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email


class UserProfileSerializer(UserProfilesSerializer):
    permissions = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', "ac_total", 'permissions', 'ac_problems', 'desc',
                  'real_name', 'avatar', 'blog', 'github', 'school', 'major', 'rating']

    def get_permissions(self, obj):
        return [permission.name for permission in obj.user.permissions.all()]

    def get_rating(self, obj):
        return obj.rating


class EditUserSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    # username = serializers.CharField(max_length=32)
    password = serializers.CharField(min_length=6, allow_blank=True, required=False, default=None)
    email = serializers.EmailField(max_length=64, allow_blank=True, required=False, default=None)
    is_disabled = serializers.BooleanField(required=False, default=False)


class EditUserProfileSerializer(serializers.Serializer):
    real_name = serializers.CharField(max_length=32, allow_null=True, required=False)
    avatar = serializers.CharField(max_length=256, allow_blank=True, required=False)
    blog = serializers.URLField(max_length=256, allow_blank=True, required=False)
    github = serializers.CharField(max_length=64, allow_blank=True, required=False)
    school = serializers.CharField(max_length=64, allow_blank=True, required=False)
    major = serializers.CharField(max_length=64, allow_blank=True, required=False)


class ApplyResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    captcha = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(min_length=6)
    captcha = serializers.CharField()


class ImageUploadForm(forms.Form):
    file = forms.FileField()


class UsernameSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    real_name = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.need_ream_name = kwargs.pop('need_real_name', False)
        super().__init__(*args, **kwargs)

    def get_real_name(self, obj):
        return obj.userprofile.real_name if self.need_ream_name else None


class RankListSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'rank', 'username', 'desc', 'ac_total', 'rating']

    def get_id(self, obj):
        return obj.user.id

    def get_username(self, obj):
        return obj.user.username

    def get_rank(self, obj):
        count = UserProfile.objects.filter(rating__gt=obj.rating).count()
        count += UserProfile.objects.filter(rating=obj.rating).filter(ac_total__gt=obj.ac_total).count()
        return count + 1


class RegistrantsSerializer(serializers.ModelSerializer):
    school = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'school', 'rating']

    def get_school(self, obj):
        return obj.userprofile.school

    def get_rating(self, obj):
        return obj.userprofile.rating
