from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from utils.models import UuidModel, BaseModel


class CustomUserManager(BaseUserManager):
    """
    自定义用户管理器，用于创建用户和超级用户
    """

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("用户必须有一个电子邮件地址")

        email = self.normalize_email(email)

        # 确保 is_admin 字段有值
        is_admin = extra_fields.get('is_admin')
        if is_admin is None:
            raise ValueError("用户必须指定 is_admin 值")

        # 创建用户
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", 1)  # 超级管理员 is_admin = 1

        if extra_fields.get("is_staff") is not True:
            raise ValueError("超级用户必须设置 is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("超级用户必须设置 is_superuser=True.")
        if extra_fields.get("is_admin") != 1:
            raise ValueError("超级用户的 is_admin 值必须为 1.")

        return self.create_user(email, username, password, **extra_fields)


class Employee(BaseModel):
    employee_code = models.CharField(
        unique=True,
        max_length=20,  # 可以设置最大长度为20，具体长度视编码需求而定
        verbose_name="员工编码",
        null=False
    )
    employee_name = models.CharField(
        max_length=50,
        verbose_name="员工姓名",  # 修正注释为"员工姓名"
        null=False
    )
    phone_number = models.CharField(
        max_length=11,
        verbose_name="手机号",
        null=False,
        unique=True  # 确保手机号唯一
    )

    class Meta:
        verbose_name = "员工"
        verbose_name_plural = "员工列表"

    def __str__(self):
        return self.employee_name


class Customer(BaseModel):
    customer_code = models.CharField(
        unique=True,
        max_length=6,  # 设置定长为6
        verbose_name="客户代码",
        validators=[MinLengthValidator(6)],  # 设置最小长度为6
        help_text="类型+年+XX（例如：A02160）"
    )
    company_name = models.CharField(
        max_length=100,
        verbose_name="公司名称",
        null=False
    )
    tax_code = models.CharField(
        unique=True,
        max_length=20,
        verbose_name="纳税人识别号",
        null=False
    )
    company_bank = models.CharField(
        max_length=20,
        verbose_name="开户银行",
        null=False
    )
    bank_account = models.CharField(
        max_length=30,
        verbose_name="银行账户",
        null=False
    )
    address = models.CharField(
        max_length=50,
        verbose_name="经营地址",
        null=False
    )
    legal_representative = models.CharField(
        max_length=16,
        verbose_name="法定代表人",
        null=False
    )
    postal_code = models.CharField(
        max_length=10,
        verbose_name="邮政编码",
        null=False
    )
    abbreviation = models.CharField(
        max_length=20,
        verbose_name="公司简称",
        null=False,
        help_text="公司简称"
    )
    contact_phone = models.CharField(
        max_length=11,
        verbose_name="联系电话",
        null=False
    )
    fixed_phone = models.CharField(
        max_length=20,
        verbose_name="固定电话",
        null=False
    )
    status = models.SmallIntegerField(
        verbose_name="客户状态",
        choices=[
            (1, "在园区"),
            (0, "关闭")
        ],
        null=False
    )

    class Meta:
        verbose_name = "客户"
        verbose_name_plural = "客户列表"

    def __str__(self):
        return self.company_name


class User(AbstractBaseUser, PermissionsMixin):
    """
    自定义用户表, 实现auth鉴权与权限管理, 实现自定义字段(会自动补上password与last_login字段)

    """

    avatar = models.CharField(max_length=100, unique=False, default=None, null=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.ManyToManyField("system.Role", verbose_name=("角色"), blank=True)
    is_admin = models.IntegerField(default=1)  # 1 为系统超级管理原 2 为园区，3 为客户

    # 外键关联设置
    park_employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'oauth_users'
        verbose_name = '系统登录用户'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username

    objects = CustomUserManager()
    USERNAME_FIELD = "email"  # 用于登录的字段
    REQUIRED_FIELDS = ["username"]  # 创建超级用户时必须输入的字段

    def save(self, *args, **kwargs):
        if self.is_admin == 2 and self.park_employee is None:
            raise ValueError("园区员工不能为空")
        elif self.is_admin == 3 and self.customer is None:
            raise ValueError("客户不能为空")
        super().save(*args, **kwargs)

    def _get_user_permissions(self):
        # 获取用户权限
        permissions = list(filter(None, set(self.role.values_list('menu__name', flat=True))))
        if 'admin' in self.role.values_list('name', flat=True):
            permissions.append('admin')
        return permissions

    def get_related_info(self):
        """
        根据 is_admin 字段返回对应的员工或客户信息
        """
        if self.is_admin == 1:
            return {
                'id': self.pk,
                'username': self.username,
                'email': self.email,
                'is_superuser': self.is_superuser
            }  # 1是系统管理员没有对应的用户

        if self.is_admin == 2:
            if self.park_employee:
                return {
                    'id': self.pk,
                    'username': self.username,
                    'email': self.email,
                    'employee_name': self.park_employee.employee_name,
                    'mobile': self.park_employee.mobile  # 确保 Employee 模型中有 `mobile` 字段
                }
            else:
                return None  # 如果没有关联的员工

        elif self.is_admin == 3:
            if self.customer:
                return {
                    'id': self.pk,
                    'username': self.username,
                    'email': self.email,
                    'permissions': self._get_user_permissions(self),
                    'company_name': self.customer.company_name,
                    'abbreviation': self.customer.abbreviation,
                    'legal_representative': self.customer.legal_representative,
                    'contact_phone': self.customer.contact_phone
                }
            else:
                return None  # 如果没有关联的客户

        return None  # 其他情况，返回 None
