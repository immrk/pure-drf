from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter
from .views import PermissionView

# 使用path创建路径，调用视图类PermissionView的as_view方法
urlpatterns = [
    path("permission/", PermissionView.as_view(), name="permission"),
]
