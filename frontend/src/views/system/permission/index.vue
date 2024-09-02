<template>
  <div class="container">
    <el-card shadow="never" class="left">
      <template #header>
        <div class="card-header">
          <span>群组选择</span>
        </div>
      </template>
      <!-- 侧边栏：群组管理 -->
      <div>
        <el-input
          v-model="groupSelectShow"
          placeholder="请选择群组"
          :disabled="true"
        />
        <div class="selector">
          <div v-for="item in groupList" :key="item.id">
            <el-radio
              v-model="groupSelect"
              :label="item.id"
              size="large"
              @change="selectChange"
              >{{ item.name_zh }}</el-radio
            >
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
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";

defineOptions({
  name: "permissionManage"
});

const groupSelectShow = ref("");

const groupSelect = ref(null);

const groupList = ref([
  {
    id: 1,
    name: "admin",
    name_zh: "管理员"
  },
  {
    id: 2,
    name: "staff",
    name_zh: "员工"
  },
  {
    id: 3,
    name: "user",
    name_zh: "用户"
  }
]);

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

const selectChange = () => {
  groupSelectShow.value = groupList.value.find(
    group => group.id === groupSelect.value
  ).name_zh;
};
</script>

<style scoped>
.container {
  width: 100%;
  /* height: 100%; */
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 20px;
}

.selector {
  padding: 5px;
  margin-top: 10px;
  height: 300px !important;
  width: 250px;
  border-radius: 5px;
  height: 100%;
  background-color: var(--el-bg-color-page);
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
