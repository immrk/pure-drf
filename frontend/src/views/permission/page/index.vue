<script setup lang="ts">
import { initRouter } from "@/router/utils";
import { storageLocal } from "@pureadmin/utils";
import { type CSSProperties, ref, computed } from "vue";
import { useUserStoreHook } from "@/store/modules/user";
import { usePermissionStoreHook } from "@/store/modules/permission";

defineOptions({
  name: "PermissionPage"
});

const elStyle = computed((): CSSProperties => {
  return {
    width: "85vw",
    justifyContent: "start"
  };
});

const email = ref(useUserStoreHook()?.email);
</script>

<template>
  <div>
    <el-card shadow="never" :style="elStyle">
      <template #header>
        <div class="card-header">
          <span>页面权限与菜单配置</span>
          <el-button type="primary" style="margin-left: 10px">
            新增页面
          </el-button>
        </div>
      </template>
    </el-card>
  </div>
</template>
