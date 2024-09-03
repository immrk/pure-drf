<template>
  <div>
    <div class="container">
      <el-card shadow="never" class="left">
        <template #header>
          <div style="display: flex; justify-content: space-between">
            <span>群组选择</span>
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
          v-model="value"
          :data="data"
          :titles="['可选权限', '已选权限']"
        />
        <div class="buttom">
          <el-button type="primary">保存</el-button>
          <el-button>撤销</el-button>
        </div>
      </el-card>
    </div>
    <!-- 新增群组弹出框 -->
    <el-dialog v-model="addGroupShow" title="新增群组" width="30%">
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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { getGroups, postGroup, deletGroup } from "@/api/system";
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

interface Option {
  key: number;
  label: string;
  disabled: boolean;
}

const generateData = () => {
  const data: Option[] = [];
  for (let i = 1; i <= 15; i++) {
    data.push({
      key: i,
      label: `Option ${i}`,
      disabled: i % 4 === 0
    });
  }
  return data;
};

const data = ref<Option[]>(generateData());
const value = ref([]);

// 对象选择赋值函数
const selectChange = () => {
  groupSelectShow.value = groupList.value.find(
    group => group.id === groupSelect.value
  );
};

// 获取对象列表函数
const getGroupsData = () => {
  getGroups()
    .then(data => {
      console.log(data);

      groupList.value = data.data;
    })
    .catch(error => {});
};

// 增加对象列表
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

// 删除对象列表
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

onMounted(() => {
  getGroupsData();
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
  width: 250px;
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
  width: 300px;
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

.buttom {
  margin-top: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}
</style>
