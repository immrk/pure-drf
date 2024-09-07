from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()  # 获取自定义的用户模型


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器，用于创建和检索用户"""

    class Meta:
        model = User
        fields = ("id", "email", "username", "avatar", "password", "is_active", "last_login")
        extra_kwargs = {"password": {"write_only": True}}  # 设置密码为只写字段

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
