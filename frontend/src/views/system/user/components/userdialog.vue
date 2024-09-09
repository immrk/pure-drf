<template>
  <el-dialog v-model="dialogVisible" :title="props.isEditMode ? '编辑用户' : '创建用户'" :width="deviceDetection() ? '90%' : '50%'" @open="handleOpen" @close="handleCancel">
    <el-form ref="userForm" :model="userData" label-width="80px" label-position="left">
      <el-form label-width="80px" :inline="true" label-position="left">
        <el-form-item label="用户名">
          <el-input v-model="userData.username" />
        </el-form-item>
        <el-form-item label="昵称">
          <el-input v-model="userData.nickname" />
        </el-form-item>
      </el-form>
      <el-form label-width="80px" :inline="true" label-position="left">
        <el-form-item label="邮箱">
          <el-input v-model="userData.email" />
        </el-form-item>
        <el-form-item :label="props.isEditMode ? '重设密码' : '设置密码'">
          <el-input v-model="userData.password" type="password" />
        </el-form-item>
      </el-form>
      <el-form-item label="所属部门" prop="parent">
        <el-cascader v-model="userData.dept_id" :options="deptData" :props="{ value: 'id', label: 'name', children: 'children', checkStrictly: true }" clearable filterable placeholder="无所属部门" />
      </el-form-item>
      <el-form-item label="激活状态">
        <el-switch v-model="userData.status" :active-value="true" :inactive-value="false" />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleConfirm">确认</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import { cloneDeep, deviceDetection } from "@pureadmin/utils";
import { handleTree } from "@/utils/tree";
import { message } from "@/utils/message";
import { getDepartList } from "@/api/system";

// 接收父组件传递的 props
const props = defineProps({
  visible: Boolean,
  user: Object,
  isEditMode: Boolean
});

const emit = defineEmits(["update:visible", "save", "cancel"]);

// 本地状态和引用
const dialogVisible = ref(props.visible);
const userData = ref({}); // 创建一个可变的本地用户数据对象
const deptData = ref([]);

// 打开对话框时，重置用户数据
const handleOpen = () => {
  userData.value = cloneDeep(props.user);
  getDepart();
};

// 处理确认操作
const handleConfirm = () => {
  emit("save", props.isEditMode ? "update" : "create", userData.value); // 向父组件发送保存事件并传递用户数据
  dialogVisible.value = false; // 关闭对话框
  emit("update:visible", false);
};

// 处理取消操作
const handleCancel = () => {
  emit("cancel"); // 向父组件发送取消事件
  dialogVisible.value = false; // 关闭对话框
  emit("update:visible", false);
};

// 获取部门数据
function getDepart() {
  // 获取部门数据
  getDepartList().then(res => {
    console.log(res.data);

    deptData.value = handleTree(res.data, "id", "parent", "children"); // 处理列表成树形数据
    console.log(deptData.value);
  });
}

watch(
  () => props.visible,
  newVal => {
    dialogVisible.value = newVal;
  }
);
</script>

<style lang="scss" scoped>
.dialog-footer {
  text-align: right;
}
</style>
