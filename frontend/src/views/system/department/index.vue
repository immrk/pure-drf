<template>
  <div class="maincontent">
    <!-- 筛选搜索区域 -->
    <div class="top">
      <el-form ref="formRef" :inline="true" :model="form" class="searchform">
        <el-form-item label="部门名称：" prop="name">
          <el-input v-model="form.name" placeholder="请输入部门名称" clearable class="!w-[180px]" />
        </el-form-item>
        <el-form-item label="状态：" prop="status">
          <el-select v-model="form.status" placeholder="请选择" clearable class="!w-[180px]">
            <el-option label="已启用" value="1" />
            <el-option label="已禁用" value="0" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :icon="useRenderIcon('ri:search-line')" :loading="loading" @click="onSearch"> 搜索 </el-button>
          <el-button :icon="useRenderIcon('ri:refresh-line')" @click="resetForm(formRef)"> 重置 </el-button>
        </el-form-item>
      </el-form>
    </div>
    <!-- 表格数据区域 -->
    <div ref="tableContainer" class="table">
      <el-table :data="dataList" style="width: 100%; margin-bottom: 20px" row-key="id" lazy :height="tableMaxHeight">
        <el-table-column label="" align="center" width="30px" />
        <el-table-column prop="id" label="部门ID" align="center" />
        <el-table-column prop="name" label="名称" align="center" />
        <el-table-column prop="sort" label="排序" sortable align="center" />
        <el-table-column prop="status" label="状态" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status ? 'success' : 'danger'">{{ row.status ? "已启用" : "已禁用" }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" fixed="right" min-width="150px">
          <template #header>
            <el-button type="primary" size="small" @click="handleCreat()">新增</el-button>
          </template>
          <template #default="{ row }">
            <el-button type="text" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="text" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <!-- 部门新建/编辑弹窗 -->
    <deptdialog v-model:visible="isDialogVisible" :dept="selectedDept" :is-edit-mode="isEditMode" :deptTree="dataList" @update:visible="isDialogVisible = $event" @save="handleSave" @cancel="handleCancel" />
  </div>
</template>

<script setup lang="ts">
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { ref, reactive, onMounted, onBeforeUnmount, nextTick } from "vue";
import { handleTree } from "@/utils/tree";
import deptdialog from "./components/deptdialog.vue";

const formRef = ref(null);

defineOptions({
  name: "department"
});

// 筛选过滤器数据
const form = reactive({
  name: "",
  status: ""
});
const loading = ref(false);
const dataList = ref([]);
const tableMaxHeight = ref(0); // 表格最大高度
const tableContainer = ref(null); // 表格容器

// 计算表格高度的函数
const calculateTableHeight = () => {
  nextTick(() => {
    if (tableContainer.value) {
      // 获取父容器的高度
      const parentHeight = tableContainer.value.clientHeight;
      tableMaxHeight.value = parentHeight; // 设置表格最大高度
    }
  });
};

// 重置表单函数
const resetForm = formEl => {
  if (!formEl) return;
  formEl.resetFields();
  onSearch();
};

// 搜索数据函数
async function onSearch() {
  loading.value = true;
  // 模拟获取部门数据
  const newData = [
    {
      name: "上海公司",
      parentId: 0,
      id: 100,
      sort: 0,
      type: 1, // 1 公司 2 分公司 3 部门, 用于在组件内控制icon显示
      status: true
    },
    {
      name: "部门1",
      parentId: 100,
      id: 101,
      sort: 0,
      type: 3, // 1 公司 2 分公司 3 部门, 用于在组件内控制icon显示
      status: true
    }
  ];
  dataList.value = handleTree(newData); // 处理列表成树形数据
  loading.value = false;
}

// 编辑用户点击事件函数
function handleEdit(row) {
  console.log("编辑部门", row);
  selectedDept.value = row;
  isEditMode.value = true;
  isDialogVisible.value = true;
}

// 新增用户点击事件函数
function handleCreat() {
  console.log("新增部门");
  selectedDept.value = {};
  isEditMode.value = false;
  isDialogVisible.value = true;
}

// 删除用户点击事件函数
function handleDelete(row) {
  console.log("删除用户", row);
}

// 弹窗相关
const isDialogVisible = ref(false);
const isEditMode = ref(false);
const selectedDept = ref({});
const handleSave = (type, data) => {
  console.log("保存", type, data);
};
const handleCancel = () => {
  console.log("取消");
};

onMounted(() => {
  // 计算表格高度的函数并挂载监听事件
  calculateTableHeight();
  window.addEventListener("resize", calculateTableHeight);
  // 初始化表格数据
  onSearch();
});

// 在组件卸载前移除监听器
onBeforeUnmount(() => {
  window.removeEventListener("resize", calculateTableHeight);
});
</script>

<style lang="scss" scoped>
.main-content {
  margin: 24px 24px 0 !important;
}

.maincontent {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 141px);
}

.searchform {
  background-color: var(--el-bg-color);
  /* padding: 10px; */
  .el-form-item {
    margin: 10px;
  }
}

.table {
  flex: 1;
  margin-top: 10px;
  background-color: var(--el-bg-color);
  height: 100%;
  /* 解决element表格在flex布局下无法自适应窗口宽度缩小的问题 */
  position: relative;
  .el-table {
    position: absolute;
  }
}
</style>
