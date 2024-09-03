项目地址：https://github.com/immrk/pure-drf

# 1 前端

## 1.1 登录鉴权

为适配不同项目用户数据表的不同字段，需要对pinia的数据模型以及登录验证的字段(用户名/邮箱/手机号 等)进行修改

# 2 后端

## 2.1 自定义用户数据与token鉴权

### 2.1.1 数据模型

文件地址：backend\apps\user\models.py

1. 自定义用户管理器，用于创建适配自定义用户数据模型的用户和超级用户
2. 承接auth的AbstractBaseUser, 补充自定义用户表字段

### 2.1.2 自定义序列化器

文件地址：backend\apps\user\serializers.py

包括用户数据序列化器与登录表单数据序列化器

用户序列化器中重写creat和update方法，采用set_password自动对密码进行加密存储

### 2.1.3 创建用户数据接口与自定义登录接口

文件地址：backend\apps\user\views.py

1. 自定义登录接口，与pure模板登录数据格式进行了统一
2. creat方法，后期用于注册接口，不作鉴权；其余接口需要鉴权，同时禁用delete接口
3. 后端返回的字符串时间，前端默认为北京时间，所以后端过期时间请返回北京时间+8小时字符串

### 2.1.4 配置路径

文件地址：backend\apps\user\urls.py

1. 使用DefaultRouter便捷创建modelviewset的路由
2. 不采用鉴权的接口暂时需要放置在DefaultRouter配置的前面，否则user视图改写的鉴权函数(get_permissions)将干扰后续接口(修改计划：后续将get_permissions转移到自定义permission里，按需引入)

### 2.1.5 自定义token鉴权

文件地址：backend\utils\authenticator.py

1. 项目均采用长短token实现用户登陆状态维持；
2. 其中“登录”接口已完成对首次短token与长token的分发，还需要对token更新接口进行自定义；
3. 通过承接TokenRefreshView，改写post请求方法，实现token刷新返回数据格式更改，适配pure模板

## 2.3 动态路由

pure项目采用"动态路由"，通过后端返回路由，再在前端进行渲染；为此需要在后端配置路由数据表与接口，并实现根据权限管理返回的路由数据

# 3 数据结构

## 3.1 用户表

drf默认用户表字段不能满足各类项目需求，经过承接原用户表再自定义后，得到以下数据结构：

其中 id, password, last_login均可由auth自动创建

```
CREATE TABLE "user_user" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "password" varchar(128) NOT NULL, 
    "last_login" datetime NULL, 
    "is_superuser" bool NOT NULL, 
    "username" varchar(100) NOT NULL UNIQUE, 
    "email" varchar(254) NOT NULL UNIQUE, 
    "is_active" bool NOT NULL, 
    "is_staff" bool NOT NULL, 
    "avatar" varchar(100) NULL, 
    "nickname" varchar(100) NULL)
```
