from rest_framework import serializers
from .models import Role, Menu, MenuMeta, DeptInfo


class RoleSerializer(serializers.ModelSerializer):
    """角色表序列化器"""

    menu = serializers.PrimaryKeyRelatedField(many=True, queryset=Menu.objects.all(), required=False, default=list)
    parent = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Role
        fields = ["id", "name", "code", "status", "menu", "parent"]


class MenuMetaSerializer(serializers.ModelSerializer):
    """菜单meta序列化器"""

    class Meta:
        model = MenuMeta
        fields = ["id", "title", "icon", "r_svg_name", "is_show_menu", "is_show_parent", "is_keepalive", "frame_url", "frame_loading", "transition_enter", "transition_leave", "is_hidden_tag", "fixed_tag", "dynamic_level"]


class MenuSerializer(serializers.ModelSerializer):
    """菜单/权限序列化器"""

    parent = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all(), allow_null=True, required=False)
    meta = MenuMetaSerializer(required=False, allow_null=True)

    class Meta:
        model = Menu
        fields = ["id", "parent", "menu_type", "name", "rank", "path", "component", "status", "meta", "method"]

    def create(self, validated_data):
        """重写创建方法，创建menu数据时自动创建meta数据并创建关联关系"""
        # 从请求数据中提取 meta 数据
        meta_data = validated_data.pop("meta", None)
        # 创建 MenuMeta 实例
        if meta_data:
            menu_meta = MenuMeta.objects.create(**meta_data)
        else:
            menu_meta = None
        # 创建 Menu 实例并关联 MenuMeta
        menu = Menu.objects.create(meta=menu_meta, **validated_data)
        return menu

    def update(self, instance, validated_data):
        """重写更新方法，更新menu数据时自动更新meta数据"""
        # 从请求数据中提取 meta 数据
        meta_data = validated_data.pop("meta", None)

        # 如果meta数据存在，更新现有的MenuMeta实例
        if meta_data:
            if instance.meta:
                # 更新现有的meta实例
                for attr, value in meta_data.items():
                    setattr(instance.meta, attr, value)
                instance.meta.save()
            else:
                # 如果之前没有meta实例，创建一个新的
                instance.meta = MenuMeta.objects.create(**meta_data)

        # 如果meta数据不存在，但存在一个与之关联的MenuMeta实例，将其保留
        elif instance.meta:
            pass

        # 更新Menu实例的其他字段
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class DeptInfoSerializer(serializers.ModelSerializer):
    """部门信息序列化器"""

    roles = serializers.PrimaryKeyRelatedField(many=True, queryset=Role.objects.all(), required=False, default=list)
    parent = serializers.PrimaryKeyRelatedField(queryset=DeptInfo.objects.all(), allow_null=True, required=False)

    class Meta:
        model = DeptInfo
        fields = ["id", "name", "code", "rank", "type", "parent", "status", "roles", "parent"]
