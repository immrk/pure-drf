from rest_framework import serializers
from .models import Role, Menu, MenuMeta, DeptInfo


class RoleSerializer(serializers.ModelSerializer):
    """角色表序列化器"""

    menu = serializers.PrimaryKeyRelatedField(many=True, queryset=Menu.objects.all(), required=False, default=list)
    parent = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Role
        fields = ["id", "name", "code", "status", "menu", "parent"]


class MenuSerializer(serializers.ModelSerializer):
    """菜单/权限序列化器"""

    parent = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all(), allow_null=True, required=False)
    meta = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all(), required=False)

    class Meta:
        model = Menu
        fields = ["id", "parent", "menu_type", "name", "rank", "path", "component", "status", "meta", "method"]


class MenuMetaSerializer(serializers.ModelSerializer):
    """菜单meta序列化器"""

    class Meta:
        model = MenuMeta
        fields = ["id", "title", "icon", "r_svg_name", "is_show_menu", "is_show_parent", "is_keepalive", "frame_url", "frame_loading", "transition_enter", "transition_leave", "is_hidden_tag", "fixed_tag", "dynamic_level"]


class DeptInfoSerializer(serializers.ModelSerializer):
    """部门信息序列化器"""

    roles = serializers.PrimaryKeyRelatedField(many=True, queryset=Role.objects.all(), required=False, default=list)
    parent = serializers.PrimaryKeyRelatedField(queryset=DeptInfo.objects.all(), allow_null=True, required=False)

    class Meta:
        model = DeptInfo
        fields = ["id", "name", "code", "rank", "type", "parent", "status", "roles", "parent"]
