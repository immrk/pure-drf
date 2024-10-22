# 用于自定义权限管理模型与方法，实现自定义多级权限管理
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
import re


class ActiveAndPermission(BasePermission):
    """
    自定义权限管理, 用于判断用户是否激活和是否拥有权限代码
    """

    def __init__(self, permission_code=None):
        # 存储需要的权限代码
        self.permission_code = permission_code

    def has_permission(self, request, view):
        # 判断用户是否激活
        if not request.user.is_active():
            raise PermissionDenied("用户未激活")
        # 获取请求路径, 并进行处理
        path = request.path
        # 如果请求的路径最后一部分是uuid，则去掉uuid部分
        uuid_pattern = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
        path_parts = path.rstrip("/").split("/")
        if uuid_pattern.match(path_parts[-1]):
            if path_parts:
                path = "/".join(path_parts[:-1]) + "/"
            else:
                path = "/".join(path_parts[:-1])

        # 获取请求方法
        method_map = {"get": "read", "post": "add", "put": "change", "patch": "change", "delete": "delete"}
        method = request.method.lower()
        permission_code = path + ":" + method_map.get(method)
        if request.user.has_perm(permission_code, path):
            return True
        else:
            raise PermissionDenied("用户无权限")
