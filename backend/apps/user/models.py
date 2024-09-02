from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    """
    自定义用户管理器，用于创建用户和超级用户
    """
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('用户必须有一个电子邮件地址')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('超级用户必须设置 is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('超级用户必须设置 is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    自定义用户表, 实现auth鉴权与权限管理, 实现自定义字段(会自动补上password与last_login字段)
    """
    avatar = models.CharField(max_length=100, unique=False, default=None, null=True)
    nickname = models.CharField(max_length=100, unique=False, default=None, null=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # 用于登录的字段
    REQUIRED_FIELDS = ['username']  # 创建超级用户时必须输入的字段

    def __str__(self):
        return self.username
