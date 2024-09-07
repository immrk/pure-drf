<template>
  <el-dialog v-model="dialogVisible" :title="props.isEditMode ? '编辑部门' : '创建部门'" :width="deviceDetection() ? '90%' : '50%'" @open="handleOpen" @close="handleCancel">
    <el-form ref="deptForm" :model="deptData" label-width="80px" label-position="left">
      <el-form-item label="部门名称">
        <el-input v-model="deptData.name" />
      </el-form-item>
      <el-form-item label="部门排序">
        <el-input v-model="deptData.sort" />
      </el-form-item>
      <el-form-item label="部门代码">
        <el-input v-model="deptData.code" />
      </el-form-item>
      <el-form-item label="部门类型">
        <el-select v-model="deptData.type" placeholder="请选择" clearable>
          <el-option label="公司" value="1" />
          <el-option label="分公司" value="2" />
          <el-option label="部门" value="3" />
        </el-select>
      </el-form-item>
      <!-- 父级部门 -->
      <el-form-item label="父级部门">
        <el-cascader v-model="deptData.parentId" :options="props.deptTree" :props="{ value: 'id', label: 'name', children: 'children', checkStrictly: true }" clearable filterable placeholder="无父级部门" />
      </el-form-item>
      <el-form-item label="激活状态">
        <el-switch v-model="deptData.status" :active-value="true" :inactive-value="false" />
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

// 接收父组件传递的 props
const props = defineProps({
  visible: Boolean,
  dept: Object,
  isEditMode: Boolean,
  deptTree: Array
});

const emit = defineEmits(["update:visible", "save", "cancel"]);

// 本地状态和引用
const dialogVisible = ref(props.visible);
const deptData = ref({}); // 创建一个可变的本地用户数据对象

// 打开对话框时，重置用户数据
const handleOpen = () => {
  deptData.value = cloneDeep(props.dept);
};

// 处理确认操作
const handleConfirm = () => {
  emit("save", props.isEditMode ? "update" : "create", deptData.value); // 向父组件发送保存事件并传递用户数据
  dialogVisible.value = false; // 关闭对话框
  emit("update:visible", false);
};

// 处理取消操作
const handleCancel = () => {
  emit("cancel"); // 向父组件发送取消事件
  dialogVisible.value = false; // 关闭对话框
  emit("update:visible", false);
};

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
