<template>
  <el-dialog v-model="dialogVisible" :title="props.isEditMode ? '编辑菜单/权限' : '创建菜单/权限'" :width="deviceDetection() ? '90%' : '50%'" @open="handleOpen" @close="handleCancel">
    <!-- 通用表单 -->
    <el-form ref="menuForm" :model="menuData" :rules="rules" label-width="80px" label-position="left">
      <el-form-item v-if="props.isEditMode" prop="id" label="ID">
        <el-input v-model="menuData.id" disabled />
      </el-form-item>
    </el-form>
    <!-- meta表单 -->
    <el-form v-if="props.isEditMode" ref="menuMetaForm" :model="menuData.meta" :rules="rules" label-width="80px" label-position="left">
      <el-form-item prop="meta.title" label="菜单标题">
        <el-input v-model="menuData.meta.title" />
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
import { ref, watch } from "vue";
import { cloneDeep, deviceDetection } from "@pureadmin/utils";
import { message } from "@/utils/message";

const menuForm = ref();

// 接收父组件传递的 props
const props = defineProps({
  visible: Boolean,
  menu: Object,
  isEditMode: Boolean,
  menuTree: Array
});

const emit = defineEmits(["update:visible", "save", "cancel"]);

// 本地状态和引用
const dialogVisible = ref(props.visible);
const menuData = ref({}); // 创建一个可变的本地用户数据对象

// 打开对话框时，重置用户数据
const handleOpen = () => {
  menuData.value = cloneDeep(props.menu);
};

// 处理确认操作
const handleConfirm = () => {
  menuForm.value.validate(valid => {
    if (valid) {
      emit("save", props.isEditMode ? "update" : "create", menuData.value); // 向父组件发送保存事件并传递用户数据
      dialogVisible.value = false; // 关闭对话框
      emit("update:visible", false);
    } else {
      message("请按规则填写", { type: "error" });
    }
  });
};

// 处理取消操作
const handleCancel = () => {
  menuForm.value.resetFields(); // 还原表单并清除错误提示信息
  emit("cancel"); // 向父组件发送取消事件
  dialogVisible.value = false; // 关闭对话框
  emit("update:visible", false);
};

// 表单校验规则
const rules = {
  name: [
    { required: true, message: "请输入菜单/权限名称", trigger: "blur" },
    { min: 2, max: 20, message: "菜单/权限名称长度限制2-10", trigger: "blur" }
  ],
  rank: { required: true, message: "请设置菜单/权限排序", trigger: "blur" },
  code: [
    { required: true, message: "请设置菜单/权限唯一标识代码", trigger: "blur" },
    { min: 2, max: 15, message: "菜单/权限名称限制2-15个字符", trigger: "blur" },
    { pattern: /^\w+$/, message: "请输入字母/数字/下划线", trigger: "blur" }
  ],
  type: { required: true, message: "请选择菜单/权限类型", trigger: "blur" }
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
