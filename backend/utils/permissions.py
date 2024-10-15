# 用于自定义权限管理模型与方法，实现自定义多级权限管理
from rest_framework.permissions import BasePermission


class ActiveAndCode(BasePermission):
    """
    自定义权限管理, 用于判断用户是否激活和是否拥有权限代码
    """

    def __init__(self, permission_code=None):
        # 存储需要的权限代码
        self.permission_code = permission_code

    def has_permission(self, request, view):
        # 判断用户是否激活
        if not request.user.is_active:
            return False
        # 判断用户是否拥有权限代码
        # if self.permission_code:
        #     return request.user.has_perm(self.permission_code)
        return True
