<template>
  <div>
    <div class="container">
      <el-card shadow="never" class="left">
        <template #header>
          <div style="display: flex; justify-content: space-between">
            <span>角色选择</span>
            <el-button
              type="primary"
              size="small"
              @click="
                addGroupShow = true;
                newgroup.name = '';
              "
              >新增</el-button
            >
          </div>
        </template>
        <!-- 侧边栏：群组管理 -->
        <div>
          <el-input
            v-model="groupSelectShow.name"
            placeholder="请选择群组"
            :disabled="true"
          />
          <div class="selector">
            <div v-for="item in groupList" :key="item.id">
              <div class="selectitem">
                <el-radio
                  v-model="groupSelect"
                  :value="item.id"
                  size="large"
                  @change="selectChange"
                  >{{ item.name }}</el-radio
                >
                <Icon
                  icon="material-symbols:delete-outline"
                  class="deleteIcon"
                  @click="deleteGroup(item)"
                />
              </div>
            </div>
          </div>
        </div>
      </el-card>
      <el-card shadow="never" class="setting">
        <template #header>
          <div class="card-header">
            <span>权限配置</span>
          </div>
        </template>
        <el-transfer
          v-model="permissionsValue"
          :data="permissionsData"
          :titles="['可选权限', '已选权限']"
        >
          <!-- 自定义option样式 -->
          <template #default="{ option }">
            <div class="option_custom">
              <Icon
                icon="lucide:edit"
                class="deleteIcon"
                @click="openPermissions('编辑', option.key)"
              />
              <p>{{ option.label }}</p>
            </div>
          </template>
          <template #left-footer>
            <el-button
              class="transfer-footer"
              size="small"
              @click="openPermissions('新增', 0)"
              >新增权限</el-button
            >
          </template>
        </el-transfer>
        <div class="buttom">
          <el-button type="primary">保存</el-button>
          <el-button>撤销</el-button>
        </div>
      </el-card>
    </div>
    <!-- 新增群组弹出框 -->
    <el-dialog v-model="addGroupShow" title="新增角色" width="30%">
      <el-input
        v-model="newgroup.name"
        placeholder="请输入需要新增的群组名称"
      />
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addGroupShow = false">取消</el-button>
          <el-button type="primary" @click="addGroup">确认</el-button>
        </span>
      </template>
    </el-dialog>
    <!-- 编辑权限弹出框 -->
    <el-dialog
      v-model="PermissionsShow"
      :title="PermissionsOperation + '权限'"
      width="30%"
      @open="getSelectPermission"
    >
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="PermissionsShow = false">取消</el-button>
          <el-button type="primary" @click="PermissionsShow = false"
            >确认</el-button
          >
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { getGroups, postGroup, deletGroup } from "@/api/system";
import { getPermissions } from "@/api/system";
import { message } from "@/utils/message";
import { Icon } from "@iconify/vue";
import { ElMessageBox } from "element-plus";

defineOptions({
  name: "permissionManage"
});

const groupSelectShow = ref({
  id: 0,
  name: ""
});

const groupSelect = ref(null);

const groupList = ref([]);

const newgroup = ref({
  name: ""
});

const addGroupShow = ref(false);

const originalPermissions = ref([]);
const permissionsData = ref([]);
const permissionsValue = ref([]);

const PermissionsShow = ref(false);
const PermissionsOperation = ref("");
const editPermissionId = ref(0);
const editPermissionData = ref({});

// 角色选择赋值函数
const selectChange = () => {
  groupSelectShow.value = groupList.value.find(
    group => group.id === groupSelect.value
  );
};

// 获取角色列表函数
const getGroupsData = () => {
  getGroups()
    .then(data => {
      console.log(data);

      groupList.value = data.data;
    })
    .catch(error => {});
};

// 增加角色
const addGroup = () => {
  if (newgroup.value.name != "") {
    postGroup(newgroup.value)
      .then(data => {
        message("新增成功", { type: "success" });
        getGroupsData();
        addGroupShow.value = false;
      })
      .catch(error => {
        const errorMessage = error.response.data.msg
          ? error.response.data.msg
          : "新增失败";
        message(errorMessage, { type: "error" });
      });
  } else {
    message("名称不得为空", { type: "error" });
  }
};

// 删除角色
const deleteGroup = item => {
  ElMessageBox.confirm(
    "该操作将同时删除该角色已配置权限信息，是否确认删除",
    "警告",
    {
      confirmButtonText: "确认删除"
    }
  ).then(() => {
    deletGroup(item.id)
      .then(data => {
        message("删除成功", { type: "success" });
        getGroupsData();
      })
      .catch(error => {
        const errorMessage = error.response.data.msg
          ? error.response.data.msg
          : "删除失败";
        message(errorMessage, { type: "error" });
      });
  });
};

// 获取可选权限列表
const getPermissionsData = () => {
  getPermissions()
    .then(data => {
      originalPermissions.value = data.data;
      // 将data.data转换为el-transfer组件需要的格式
      const newData = originalPermissions.value.map(item => {
        return {
          key: item.id,
          label: item.name,
          disabled: false
        };
      });
      permissionsData.value = newData;
    })
    .catch(error => {});
};

// 权限新建/编辑弹窗打开函数(根据传入值判断)
const openPermissions = (operation: string, id: number) => {
  PermissionsOperation.value = operation;
  editPermissionId.value = id;
  PermissionsShow.value = true;
};

// 打开权限弹窗时的事件
const getSelectPermission = () => {
  if (PermissionsOperation.value === "编辑") {
    // 根据id从originalPermissions里面找到对应的权限数据，并赋值给editPermissionData
    editPermissionData.value = originalPermissions.value.find(
      item => item.id === editPermissionId.value
    );
    console.log(editPermissionData.value);
  }
};

onMounted(() => {
  getGroupsData();
  getPermissionsData();
});
</script>

<style scoped>
.container {
  width: 100%;
  /* height: 100%; */
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 20px;
  /* padding: 20px; */
}

.selector {
  padding: 5px;
  margin-top: 10px;
  height: 300px !important;
  width: 200px;
  border-radius: 5px;
  height: 100%;
  box-shadow: 0 0 0 1px var(--el-disabled-border-color) inset;
}

.selectitem {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 0 5px;
}

.deleteIcon {
  color: #e7a0a0;
  cursor: pointer;
}

.deleteIcon:hover {
  color: #e05d5d;
  cursor: pointer;
}

.setting {
  flex: 1;
  /* margin: 0 20px; */
}

.el-transfer {
  display: flex;
  justify-content: space-evenly;
  /* gap: 10px; */
}

.el-transfer :deep().el-transfer-panel {
  /* border-radius: 10px; */
  width: 400px;
}

.el-transfer :deep().el-transfer__buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.el-transfer :deep().el-transfer__button:nth-child(2) {
  margin: 50px 0 0 0;
}

.el-transfer
  :deep().el-transfer-panel
  .el-transfer-panel__header
  .el-checkbox
  .el-checkbox__label {
  color: #575757;
  font-size: 13px;
  font-weight: normal;
}

.el-transfer :deep().el-checkbox {
  --el-checkbox-font-size: 16px;
  --el-text-color-regular: #575757;
}

.option_custom {
  display: flex;
  gap: 10px;
  align-items: center;
}

.transfer-footer {
  margin-left: 15px;
  padding: 6px 5px;
}

.buttom {
  margin-top: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}
</style>
