from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()  # 获取自定义的用户模型


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器，用于创建和检索用户"""

    roles = serializers.SerializerMethodField()  # 定义 roles 为 SerializerMethodField

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "nickname",
            "avatar",
            "password",
            "is_active",
            "last_login",
            "roles",
        )
        extra_kwargs = {"password": {"write_only": True}}  # 设置密码为只写字段

    def get_roles(self, obj):
        """根据用户的 is_staff 和 is_supervisor 字段生成角色列表"""
        roles = []
        if getattr(obj, "is_superuser", False):
            roles.append("admin")
        if getattr(obj, "is_staff", False):
            roles.append("staff")
        if not roles:  # 如果既不是管理员也不是监督者
            roles.append("user")
        return roles

    def create(self, validated_data):
        """重写创建方法以使用set_password方法来创建用户"""
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  # 使用set_password来设置密码
        user.save()
        return user

    def update(self, instance, validated_data):
        """重写更新方法，以便在更新密码时也能使用set_password"""
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
