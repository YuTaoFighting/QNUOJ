from rest_framework import serializers
from django import forms
from account.models import User, UserProfile


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    tfa_code = serializers.CharField(required=False, allow_blank=True)


class UsernameOrEmailCheckSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(min_length=6)
    email = serializers.CharField(max_length=64)
    captcha = serializers.CharField()


class UserChangeEmailSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    new_email = serializers.CharField(max_length=64)
    tfa_code = serializers.CharField(required=False, allow_blank=True)


class GenerateUserSerializer(serializers.ModelSerializer):
    prefix = serializers.CharField(max_length=16, allow_blank=True)
    suffix = serializers.CharField(max_length=16, allow_blank=True)
    number_from = serializers.IntegerField()
    number_to = serializers.IntegerField()
    password_length = serializers.IntegerField(max_value=16, default=8)


class ImportUserSerializer(serializers.ModelSerializer):
    users = serializers.ListField(
        child=serializers.ListField(child=serializers.CharField(max_length=64))
    )


class UserAdminSerializer(serializers.ModelSerializer):
    real_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'real_name', 'create_time', 'is_disabled']

    def get_real_name(self, obj):
        return obj.userprofile.realname


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'create_time', 'is_disabled']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer
    real_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.show_real_name = kwargs.pop('show_real_name', False)
        super(UserProfileSerializer, self).__init__(*args, **kwargs)

    def get_real_name(self, obj):
        return obj.real_name if self.show_real_name else None


class EditUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=32)
    real_name = serializers.CharField(max_length=32, allow_blank=True, allow_null=True)
    password = serializers.CharField(min_length=6, allow_blank=True, required=False, default=None)
    email = serializers.EmailField(max_length=64)
    is_disabled = serializers.BooleanField()


class EditUserProfileSerializer(serializers.ModelSerializer):
    real_name = serializers.CharField(max_length=32, allow_null=True, required=False)
    avatar = serializers.CharField(max_length=256, allow_blank=True, required=False)
    blog = serializers.URLField(max_length=256, allow_blank=True, required=False)
    github = serializers.CharField(max_length=64, allow_blank=True, required=False)
    school = serializers.CharField(max_length=64, allow_blank=True, required=False)
    major = serializers.CharField(max_length=64, allow_blank=True, required=False)


class ApplyResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    captcha = serializers.CharField()


class ResetPasswordSerializer(serializers.ModelSerializer):
    token = serializers.CharField()
    password = serializers.CharField(min_length=6)
    captcha = serializers.CharField()


class ImageUploadForm(forms.Form):
    file = forms.FileField()


class UsernameSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    real_name = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.need_ream_name = kwargs.pop('need_real_name', False)
        super().__init__(*args, **kwargs)

    def get_real_name(self, obj):
        return obj.userprofile.real_name if self.need_ream_name else None


class RankInfoSerializer(serializers.ModelSerializer):
    user = UsernameSerializer

    class Meta:
        model = UserProfile
        fields = '__all__'