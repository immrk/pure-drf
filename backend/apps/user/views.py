from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model, authenticate, login
from .serializers import UserSerializer, LoginSerializer
from utils.pagination import (
    CustomPageNumberPagination,
    CustomLimitOffsetPagination,
    CustomCursorPagination,
)
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    用户视图集，支持用户的CRUD操作
    """

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination

    def get_permissions(self):
        """
        根据不同的操作来设置权限
        """
        if self.action in ["create"]:
            # 注册新用户时允许任何人访问
            permission_classes = [AllowAny]
        else:
            # 对于其他操作，要求用户认证
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        # 重写禁用删除功能, 用户注销逻辑另写
        return Response(
            {"detail": "Delete operation is not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    # 自定义新方法，当使用DefaultRouter配置路由时，会自动使用函数名创建路径为 /get_self/
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def self(self, request):
        """
        根据 token 获取请求用户数据
        """
        user = request.user  # 从请求中获取当前用户
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class LoginView(APIView):
    """
    登录类，调用auth的认证登录与JWT逻辑
    """

    permission_classes = [AllowAny]
    authentication_classes = []  # 该接口不需要鉴权

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "success": True,
                        "data": {
                            "refreshToken": str(refresh),
                            "accessToken": str(refresh.access_token),
                            "expires": "2030/10/30 00:00:00"
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"msg": "登录信息错误"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
