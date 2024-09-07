from django.contrib import admin
from django.contrib.auth import get_user_model
from apps.system.models import Role, Menu, MenuMeta
from apps.user.models import Customer,Employee

Users = get_user_model()
# Register your models here.

admin.site.register(Users)
admin.site.register(Role)
admin.site.register(Menu)
admin.site.register(MenuMeta)
admin.site.register(Customer)
admin.site.register(Employee)