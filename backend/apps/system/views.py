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

    queryset = Menu.objects.all()
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
        menus = Menu.objects.filter(role__in=roles, menu_type=Menu.MenuChoices.MENU).distinct()
        print("Queryset of menus:", menus)
        # 模拟动态生成的路由数据
        serializer = RouteSerializer(menus, many=True)

        permission_router = {
            "path": "/permission",
            "meta": {"title": "权限管理", "icon": "ep:lollipop", "rank": 2},
            "children": [
                {"path": "/permission/page/index", "name": "PermissionPage", "meta": {"title": "页面权限", "roles": ["b3223970-2c59-444a-8e21-153a94afe909", "98ad15b7-6433-4729-8fc0-5b941e33b39c"]}},
                {
                    "path": "/permission/button",
                    "meta": {"title": "按钮权限", "roles": ["b3223970-2c59-444a-8e21-153a94afe909", "98ad15b7-6433-4729-8fc0-5b941e33b39c"]},
                    "children": [
                        {"path": "/permission/button/router", "component": "permission/button/index", "name": "PermissionButtonRouter", "meta": {"title": "路由返回按钮权限", "auths": ["permission:btn:add", "permission:btn:edit", "permission:btn:delete"]}},
                        {"path": "/permission/button/login", "component": "permission/button/perms", "name": "PermissionButtonLogin", "meta": {"title": "登录接口返回按钮权限"}},
                    ],
                },
            ],
        }

        # 返回 JSON 响应
        # return CustomResponse(success=True, data=serializer.data, msg="成功获取动态路由")
        return CustomResponse(success=True, data=[permission_router], msg="成功获取动态路由")
