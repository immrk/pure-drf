# Generated by Django 4.1.8 on 2024-09-04 09:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('menu_type', models.SmallIntegerField(choices=[(0, 'Directory'), (1, 'Menu'), (2, 'Permission')], default=0, verbose_name='菜单类型')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='组件名称/权限代码')),
                ('rank', models.IntegerField(default=9999, verbose_name='优先级')),
                ('path', models.CharField(max_length=255, verbose_name='路由地址/api地址')),
                ('component', models.CharField(blank=True, max_length=255, null=True, verbose_name='组件地址')),
                ('is_active', models.BooleanField(default=True, verbose_name='激活')),
                ('method', models.CharField(blank=True, choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE'), ('PATCH', 'PATCH')], max_length=10, null=True, verbose_name='Method')),
            ],
            options={
                'verbose_name': '菜单/权限',
                'verbose_name_plural': '菜单/权限',
                'ordering': ('create_time',),
            },
        ),
        migrations.CreateModel(
            name='MenuMeta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Menu title')),
                ('icon', models.CharField(blank=True, max_length=255, null=True, verbose_name='Left icon')),
                ('r_svg_name', models.CharField(blank=True, help_text='Additional icon to the right of menu name', max_length=255, null=True, verbose_name='Right icon')),
                ('is_show_menu', models.BooleanField(default=True, verbose_name='Show menu')),
                ('is_show_parent', models.BooleanField(default=False, verbose_name='Show parent menu')),
                ('is_keepalive', models.BooleanField(default=False, help_text='When enabled, the entire state of the page is saved, and when refreshed, the state is cleared', verbose_name='Keepalive')),
                ('frame_url', models.CharField(blank=True, help_text='The embedded iframe link address', max_length=255, null=True, verbose_name='Iframe URL')),
                ('frame_loading', models.BooleanField(default=False, verbose_name='Iframe loading')),
                ('transition_enter', models.CharField(blank=True, max_length=255, null=True, verbose_name='Enter animation')),
                ('transition_leave', models.CharField(blank=True, max_length=255, null=True, verbose_name='Leave animation')),
                ('is_hidden_tag', models.BooleanField(default=False, help_text='The current menu name or custom information is prohibited from being added to the TAB', verbose_name='Hidden tag')),
                ('fixed_tag', models.BooleanField(default=False, help_text='Whether the current menu name is fixed to the TAB and cannot be closed', verbose_name='Fixed tag')),
                ('dynamic_level', models.IntegerField(default=0, help_text='Maximum number of dynamic routes that can be opened', verbose_name='Dynamic level')),
            ],
            options={
                'verbose_name': 'Menu meta',
                'verbose_name_plural': 'Menu meta',
                'ordering': ('-create_time',),
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='角色名称')),
                ('code', models.CharField(max_length=128, unique=True, verbose_name='角色代码')),
                ('is_active', models.BooleanField(default=True, verbose_name='激活状态')),
                ('menu', models.ManyToManyField(blank=True, to='system.menu', verbose_name='菜单')),
            ],
            options={
                'verbose_name': '角色表',
                'verbose_name_plural': '角色表',
                'ordering': ('create_time',),
            },
        ),
        migrations.AddField(
            model_name='menu',
            name='meta',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='system.menumeta', verbose_name='Menu meta'),
        ),
        migrations.AddField(
            model_name='menu',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.menu', verbose_name='父级菜单'),
        ),
        migrations.CreateModel(
            name='DeptInfo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=128, verbose_name='Department name')),
                ('code', models.CharField(max_length=128, unique=True, verbose_name='Department code')),
                ('rank', models.IntegerField(default=99, verbose_name='Rank')),
                ('auto_bind', models.BooleanField(default=False, help_text='If the value of the registration parameter channel is consistent with the department code, the user is automatically bound to the department', verbose_name='Auto bind')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='parent_query', to='system.deptinfo', verbose_name='Superior department')),
                ('roles', models.ManyToManyField(blank=True, to='system.role', verbose_name='Role permission')),
            ],
            options={
                'verbose_name': '部门',
                'verbose_name_plural': '部门',
                'ordering': ('rank', 'create_time'),
            },
        ),
    ]
