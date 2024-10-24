<template>
  <el-dialog v-model="dialogVisible" title="创建接口权限">
    <div>
      <p>接口地址：</p>
      <el-input v-model="url" placeholder="例:/api/test/permission/ 请输入需要创建权限的接口地址" />
      <span>该操作将一键为指定接口创建增删改查四个接口权限；<br />角色若未被分配对应权限将无法调用对应接口</span>
    </div>
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
import { message } from "@/utils/message";
import { postMenu } from "@/api/system";

// 接收父组件传递的 props
const props = defineProps({
  visible: Boolean,
  parent: Object
});

const emit = defineEmits(["update:visible", "save", "cancel"]);
const url = ref("");

const dialogVisible = ref(props.visible);
const parent = ref(props.id);

const addlist = ref([
  {
    name: "查看",
    code: ":read",
    menu_type: 2,
    path: "",
    status: true,
    parent: props.parent,
    meta: {
      showLink: true,
      showParent: true,
      keepAlive: false,
      hiddenTag: false,
      fixedTag: false,
      rank: 9995
    }
  },
  {
    name: "新增",
    code: ":add",
    menu_type: 2,
    path: "",
    status: true,
    parent: props.parent,
    meta: {
      showLink: true,
      showParent: true,
      keepAlive: false,
      hiddenTag: false,
      fixedTag: false,
      rank: 9996
    }
  },
  {
    name: "修改",
    code: ":change",
    menu_type: 2,
    path: "",
    status: true,
    parent: props.parent,
    meta: {
      showLink: true,
      showParent: true,
      keepAlive: false,
      hiddenTag: false,
      fixedTag: false,
      rank: 9997
    }
  },
  {
    name: "删除",
    code: ":delete",
    menu_type: 2,
    path: "",
    status: true,
    parent: props.parent,
    meta: {
      showLink: true,
      showParent: true,
      keepAlive: false,
      hiddenTag: false,
      fixedTag: false,
      rank: 9998
    }
  }
]);

// 处理确认操作
const handleConfirm = () => {
  if (url.value === "") {
    message("请输入接口地址", { type: "error" });
    return;
  }
  // 根据输入的url，修改addlist中的path并在code前加上url
  addlist.value.forEach(item => {
    item.path = url.value;
    item.code = url.value + item.code;
  });
  console.log(addlist.value);
  postMenu(addlist.value)
    .then(res => {
      onSearch();
      message(res.msg, { type: "success" });
    })
    .catch(res => {
      console.log(res);
      message(res.response.data.msg, { type: "error" });
    });
};

// 处理取消操作
const handleCancel = () => {
  emit("update:visible", false);
};

watch(
  () => props.visible,
  newVal => {
    dialogVisible.value = newVal;
  }
);
</script>

<style lang="scss" scoped></style>
