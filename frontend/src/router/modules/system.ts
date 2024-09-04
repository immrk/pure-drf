export default {
  path: "/system",
  redirect: "/system/usermanage",
  meta: {
    icon: "ri:information-line",
    // showLink: false,
    title: "系统管理",
    rank: 1
  },
  children: [
    {
      path: "/system/usermanage",
      name: "usermanage",
      component: () => import("@/views/system/index.vue"),
      meta: {
        title: "用户管理",
        keepAlive: true
      }
    },
    {
      path: "/system/permissionManage",
      name: "permissionManage",
      component: () => import("@/views/system/permission/index.vue"),
      meta: {
        title: "菜单权限",
        keepAlive: true
      }
    }
  ]
} satisfies RouteConfigsTable;
