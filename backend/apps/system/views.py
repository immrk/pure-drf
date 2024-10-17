from .serializers import GroupSerializer, PermissionSerializer
from django.contrib.auth.models import Group, Permission
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.viewset import CustomModelViewSet
