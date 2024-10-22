# 过滤器代码文件
from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFilter(filters.FilterSet):
    """用户数据筛选器"""

    dept = filters.CharFilter(field_name="dept_id", lookup_expr="exact")
    username = filters.CharFilter(field_name="username", lookup_expr="icontains")  # 为 name 字段设置模糊查询 (icontains)
    email = filters.CharFilter(field_name="email", lookup_expr="exact")
    status = filters.CharFilter(lookup_expr="exact")  # 保持 status 精确匹配

    class Meta:
        model = User
        fields = ["dept_id", "username", "email", "status"]
