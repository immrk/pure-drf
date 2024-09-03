from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException
from .response import CustomResponse

class CustomModelViewSet(ModelViewSet):
    """
    自定义的ModelViewSet，使用CustomResponse来统一响应格式。
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return CustomResponse(success=True, data=serializer.data, msg="成功获取列表", page=request.query_params.get('page', 1), limit=request.query_params.get('limit', 10), total=self.paginator.page.paginator.count)

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse(success=True, data=serializer.data, msg="成功获取列表")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse(success=True, data=serializer.data, msg="成功获取详情")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return CustomResponse(success=True, data=serializer.data, msg="成功创建", status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return CustomResponse(success=True, data=serializer.data, msg="成功更新")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return CustomResponse(success=True, data=None, msg="成功删除", status=status.HTTP_204_NO_CONTENT)
    
    def handle_exception(self, exc):
        """
        捕获异常并返回自定义响应格式。
        """
        if isinstance(exc, APIException):
            # 如果是 DRF 的标准 API 异常类型
            response = super().handle_exception(exc)
            return CustomResponse(success=False, data=None, msg=response.data.get('detail', '发生错误'), status=response.status_code)
        else:
            # 对于非 DRF 的异常类型（例如Python的原生异常），返回500错误
            return CustomResponse(success=False, data=None, msg=str(exc), status=status.HTTP_500_INTERNAL_SERVER_ERROR)