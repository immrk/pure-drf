from rest_framework.serializers import ModelSerializer
from .serializers import GroupSerializer
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAuthenticated, AllowAny


class GroupViewSet(ModelViewSet):
    """权限表管理试图"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
