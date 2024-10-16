<template>
  <div class="maincontent">
    <!-- 路由权限 -->
    <!-- 组件方法：权限 -->
    <Auth value="permission:data:add">
      <el-card shadow="never">
        <p>组件方法：当前页面拥有权限 permission:data:add 可见</p>
        <p>Auth value="permission:data:add"</p>
      </el-card>
    </Auth>
    <div style="height: 10px" />
    <!-- 函数方法 -->
    <el-card v-if="hasAuth('permission:data:edit')" shadow="never">
      <p>函数方法：当前页面拥有权限 permission:data:edit 可见</p>
      <p>v-if="hasAuth('permission:data:edit')"</p>
    </el-card>
    <div style="height: 10px" />
    <!-- 指令方法 -->
    <el-card v-auth="'permission:data:delete'" shadow="never">
      <p>指令方法：当前页面拥有权限 permission:data:delete 可见</p>
      <p>v-auth="'permission:data:delete'"</p>
    </el-card>
    <div style="height: 10px" />
    <!-- 后端接口权限测试 -->
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span>后端接口权限测试</span>
        </div>
      </template>
      <div class="button-content">
        <p>1.拥有permission:data:get可成功回调</p>
        <el-button type="primary" @click="getData">permission:data:get</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { hasAuth, getAuths } from "@/router/utils";
import { getTestPermission } from "@/api/test";
import { message } from "@/utils/message";
import { ref } from "vue";

const getData = () => {
  getTestPermission()
    .then(res => {
      message(res.msg, { type: "success" });
    })
    .catch(err => {
      message(err.response.data.msg, { type: "error" });
    });
};
</script>

<style scoped></style>
