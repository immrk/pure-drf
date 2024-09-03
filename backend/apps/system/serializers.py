from django.contrib.auth.models import Group
from rest_framework.serializers import ModelSerializer


class GroupSerializer(ModelSerializer):
    """auth自带的Group表序列化器"""
    class Meta:
        model = Group
        fields = ['id', 'name']
