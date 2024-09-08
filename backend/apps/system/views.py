from .serializers import RoleSerializer, MenuSerializer, MenuMetaSerializer, DeptInfoSerializer
from .models import Role, Menu, MenuMeta, DeptInfo
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.viewset import CustomModelViewSet


class RoleViewSet(CustomModelViewSet):
    """角色表视图集"""

    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class MenuViewSet(CustomModelViewSet):
    """菜单/权限视图集"""

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MenuMetaViewSet(CustomModelViewSet):
    """菜单meta视图集"""

    queryset = MenuMeta.objects.all()
    serializer_class = MenuMetaSerializer


class DeptInfoViewSet(CustomModelViewSet):
    """部门信息视图集"""

    queryset = DeptInfo.objects.all()
    serializer_class = DeptInfoSerializer
