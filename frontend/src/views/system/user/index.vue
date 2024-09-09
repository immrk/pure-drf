<template>
  <div class="maincontent">
    <tree ref="treeRef" class="left" :treeData="treeData" :treeLoading="treeLoading" @tree-select="onTreeSelect" />
    <div class="right">
      <!-- 筛选搜索区域 -->
      <el-form ref="formRef" :inline="true" :model="form" class="searchform">
        <el-form-item label="用户名称：" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名称" clearable class="!w-[180px]" />
        </el-form-item>
        <el-form-item label="邮箱：" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" clearable class="!w-[180px]" />
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
      <!-- 表格数据区域 -->
      <div ref="tableContainer" class="table">
        <el-table :data="dataList" class="el-table" :height="tableMaxHeight">
          <el-table-column prop="id" label="ID" align="center" />
          <el-table-column prop="username" label="用户名称" align="center" />
          <el-table-column prop="email" label="邮箱" align="center" />
          <el-table-column prop="deptId" label="部门" align="center" />
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
    </div>
    <!-- 用户新建/编辑弹窗 -->
    <userdialog v-model:visible="isDialogVisible" :user="selectedUser" :is-edit-mode="isEditMode" @update:visible="isDialogVisible = $event" @save="handleSave" @cancel="handleCancel" />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onBeforeUnmount, nextTick } from "vue";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { isAllEmpty } from "@pureadmin/utils";
import { handleTree } from "@/utils/tree";
import tree from "./components/tree.vue";
import userdialog from "./components/userdialog.vue";
import { getUserList, putUser } from "@/api/user";
import { getDepartList } from "@/api/system";
import { message } from "@/utils/message";

defineOptions({
  name: "usermanage"
});

const formRef = ref(null);
const treeRef = ref(null);
const treeData = ref([]);
const treeLoading = ref(false);

// 筛选过滤器数据
const form = reactive({
  dept_id: "",
  username: "",
  email: "",
  status: ""
});

// 表格数据
const dataList = ref([]);
const tableMaxHeight = ref(0); // 表格最大高度
const tableContainer = ref(null); // 通过ref获取DOM元素
const loading = ref(false);
// 用户弹窗组件数据
const isDialogVisible = ref(false);
const isEditMode = ref(false);
const selectedUser = ref({});

// 编辑/新增 部门 数据过滤函数
function userFilter(data) {
  delete data.id;
  // 上传时剔除空值字段
  data = Object.fromEntries(Object.entries(data).filter(([key, value]) => !isAllEmpty(value)));
  // 若存在dept_id，则提取最后一个元素(element组件会默认携带列表)
  if (data.dept_id && Array.isArray(data.dept_id)) {
    data.dept_id = data.dept_id[data.dept_id.length - 1];
  }
  return data;
}

// 用户弹窗组件保存操作
const handleSave = (method, data) => {
  // 根据method判断是新增还是编辑
  if (method === "create") {
    const id = data.id;
    const newdata = userFilter(data);
    console.log("新增用户", method, newdata);
  } else {
    // 编辑用户
    const id = data.id;
    const newdata = userFilter(data);
    console.log("更新用户", method, newdata);
    // putUser(newdata.id, newdata).then(res => {
    //   message("更新成功", { type: "success" });
    //   onSearch();
    // });
  }
};

// 用户弹窗组件取消操作
const handleCancel = () => {
  isDialogVisible.value = false;
};

// 部门树选择事件函数
function onTreeSelect({ id, selected }) {
  form.dept_id = selected ? id : "";
  onSearch();
}

// 搜索数据函数
async function onSearch() {
  loading.value = true;
  // 获取用户数据，赋值dataList和分页
  await getUserList(form).then(res => {
    dataList.value = res.results;
    loading.value = false;
  });
}

// 重置表单函数
const resetForm = formEl => {
  if (!formEl) return;
  formEl.resetFields();
  form.dept_id = "";
  treeRef.value.onTreeReset();
  onSearch();
};

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

// 编辑用户点击事件函数
function handleEdit(row) {
  console.log("编辑用户", row);
  selectedUser.value = row;
  isEditMode.value = true;
  isDialogVisible.value = true;
}

// 新增用户点击事件函数
function handleCreat() {
  selectedUser.value = {};
  isEditMode.value = false;
  isDialogVisible.value = true;
}

// 删除用户点击事件函数
function handleDelete(row) {
  console.log("删除用户", row);
}

onMounted(async () => {
  // 计算表格高度的函数并挂载监听事件
  calculateTableHeight();
  window.addEventListener("resize", calculateTableHeight);
  // 模拟获取部门数据
  treeLoading.value = true;
  await getDepartList().then(res => {
    treeData.value = handleTree(res.data, "id", "parent", "children"); // 处理列表成树形数据
    loading.value = false;
    treeLoading.value = false;
  });
  // 搜索数据
  onSearch();
});

// 在组件卸载前移除监听器
onBeforeUnmount(() => {
  window.removeEventListener("resize", calculateTableHeight);
});
</script>

<style scoped>
.main-content {
  margin: 24px 24px 0 !important;
}

.maincontent {
  display: flex;
  flex-direction: row;
  height: calc(100vh - 141px);
}

.left {
  min-width: 200px;
  margin-right: 10px;
}

.right {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
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
