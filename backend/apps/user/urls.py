from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LoginView, AsyncRoutesView

# 创建一个DefaultRouter路由器对象, 会自动按照drf规则创建路由
router = DefaultRouter()
router.register('', UserViewSet, basename='user')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
    path('asyncroutes/', AsyncRoutesView.as_view(), name='AsyncRoutesView'),
]