from django.contrib.auth.models import Group, Permission
from rest_framework.serializers import ModelSerializer


class GroupSerializer(ModelSerializer):
    """auth自带的Group表序列化器"""
    class Meta:
        model = Group
        fields = ['id', 'name']


class PermissionSerializer(ModelSerializer):
    """auth自带的Permission表序列化器"""
    class Meta:
        model = Permission
        fields = ['id', 'content_type_id', 'name', 'codename']
