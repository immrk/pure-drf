<template>
  <el-card shadow="never">
    <template #header>
      <div class="card-header">
        <span>用户列表</span>
      </div>
    </template>
    <el-table :data="tableData" style="width: 100%">
      <el-table-column prop="id" label="用户id" align="center" />
      <el-table-column prop="username" label="用户名称" align="center" />
      <el-table-column prop="nickname" label="昵称" align="center" />
      <el-table-column prop="email" label="邮箱" align="center" width="200px" />
      <el-table-column prop="roles" label="权限角色" align="center" />
      <!-- 状态栏, "开关"展示值且可直接编辑 -->
      <el-table-column #default="scope" align="center" label="状态">
        <el-switch
          v-model="scope.row.is_active"
          active-text="启用"
          inactive-text="禁用"
          :inline-prompt="true"
          @change="handleStatusChange(scope.row)"
        />
      </el-table-column>
      <el-table-column label="操作" align="center" fixed="right" width="150px">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.$index, scope.row)"
            >编辑</el-button
          >
          <el-button
            size="small"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { type UserListResult, getUserList } from "@/api/user";

defineOptions({
  name: "usermanage"
});

const tableData = ref([]);

// 表格操作函数
const handleEdit = (index, row) => {
  console.log(index, row);
};
const handleDelete = (index, row) => {
  console.log(index, row);
};
const handleStatusChange = row => {
  console.log(row);
};

// 生命周期函数
onMounted(() => {
  getUserList().then(res => {
    console.log(res);
    tableData.value = res.results;
  });
});
</script>

<style scoped></style>
