# 自定义异常返回
from rest_framework.views import exception_handler
from .response import CustomResponse
from rest_framework import status


def custom_exception_handler(exc, context):
    # 使用默认的异常处理方法获取初始响应
    response = exception_handler(exc, context)

    if response is not None:
        # 若存在detail字段，则将其替换为msg字段
        if response.data.get("detail"):
            return CustomResponse(success=False, msg=response.data.get("detail"), status=response.status_code)
        return CustomResponse(success=False, data=response.data, msg="请求异常", status=response.status_code)

    # 返回None表示异常未被处理
    return response
