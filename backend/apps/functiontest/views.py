from django.shortcuts import render
from utils.response import CustomResponse
from rest_framework.views import APIView
from utils.decorators import require_permission


# Create your views here.
class PermissionView(APIView):
    """
    用于后端权限测试
    """

    @require_permission("permission:data:get")
    def get(self, request, *args, **kwargs):
        return CustomResponse(success=True, data=None, msg="权限测试成功")
