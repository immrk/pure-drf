from .serializers import RoleSerializer, MenuSerializer, MenuMetaSerializer, DeptInfoSerializer, RouteSerializer
from .models import Role, Menu, MenuMeta, DeptInfo
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.viewset import CustomModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import RoleFilter, MenuFilter, DeptFilter
from rest_framework.views import APIView
from utils.response import CustomResponse


class RoleViewSet(CustomModelViewSet):
    """角色表视图集"""

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoleFilter


class MenuViewSet(CustomModelViewSet):
    """菜单/权限视图集"""

    queryset = Menu.objects.all().order_by("meta__rank")
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MenuFilter


class MenuMetaViewSet(CustomModelViewSet):
    """菜单meta视图集"""

    queryset = MenuMeta.objects.all()
    serializer_class = MenuMetaSerializer


class DeptInfoViewSet(CustomModelViewSet):
    """部门信息视图集"""

    queryset = DeptInfo.objects.all()
    serializer_class = DeptInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DeptFilter


class AsyncRoutesView(APIView):
    """动态路由视图"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        roles = user.role.all()
        # 根据用户角色获取所有关联的菜单，避免重复通过 distinct 去重
        menus = Menu.objects.filter(role__in=roles, menu_type=Menu.MenuChoices.MENU).distinct().order_by("meta__rank")
        serializer = RouteSerializer(menus, many=True)
        # 返回 JSON 响应
        return CustomResponse(success=True, data=serializer.data, msg="成功获取动态路由")
