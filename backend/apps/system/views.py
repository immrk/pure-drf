from .serializers import GroupSerializer, PermissionSerializer
from django.contrib.auth.models import Group, Permission
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.viewset import CustomModelViewSet


class GroupViewSet(CustomModelViewSet):
    """权限表管理试图"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class PermissionViewSet(CustomModelViewSet):
    """权限表管理试图"""
    queryset = Permission.objects.all().order_by('id')
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]
