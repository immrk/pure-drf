import { handleTree } from "@/utils/tree"; // 将列表数据转化为tree数据
import { getKeyList, isAllEmpty, hideTextAtIndex, deviceDetection } from "@pureadmin/utils"; // pure通用函数
import { type Ref, ref, reactive, onMounted } from "vue";

export function useUser(tableRef: Ref, treeRef: Ref) {
  const treeData = ref([]);
  const dataList = ref([
    {
      username: "admin",
      nickname: "yajianke",
      email: "k13155153766@163.com",
      id: 1,
      status: 1,
      dept: {
        // 部门id
        id: 103,
        // 部门名称
        name: "研发部门"
      },
      remark: "管理员",
      createTime: 1605456000000
    }
  ]); // 用户表格数据
  const treeLoading = ref(false);
  // 筛选过滤器数据
  const form = reactive({
    deptId: "",
    username: "",
    email: "",
    status: ""
  });
  const loading = ref(false);
  const columns: TableColumnList = [
    {
      label: "勾选列", // 如果需要表格多选，此处label必须设置
      type: "selection",
      fixed: "left",
      reserveSelection: true // 数据刷新后保留选项
    },
    {
      label: "用户编号",
      prop: "id",
      width: 90
    },
    {
      label: "用户名称",
      prop: "username",
      minWidth: 130
    },
    {
      label: "用户昵称",
      prop: "nickname",
      minWidth: 130
    },
    {
      label: "部门",
      prop: "dept.name",
      minWidth: 90
    },
    {
      label: "邮箱",
      prop: "email",
      minWidth: 90
    },
    {
      label: "操作",
      fixed: "right",
      width: 180,
      slot: "operation"
    }
  ];
  const selectedNum = ref(0);

  // 部门树选择事件函数
  function onTreeSelect({ id, selected }) {
    form.deptId = selected ? id : "";
  }

  //
  async function onSearch() {
    loading.value = true;
    // 模拟获取用户数据，赋值dataList和分页
    setTimeout(() => {
      loading.value = false;
    }, 500);
  }

  const resetForm = formEl => {
    if (!formEl) return;
    formEl.resetFields();
    form.deptId = "";
    treeRef.value.onTreeReset();
    onSearch();
  };

  onMounted(async () => {
    // 模拟获取部门数据
    const data = [
      {
        name: "上海公司",
        parentId: 0,
        id: 100,
        sort: 0,
        type: 1 // 1 公司 2 分公司 3 部门, 用于在组件内控制icon显示
      },
      {
        name: "部门1",
        parentId: 100,
        id: 101,
        sort: 0,
        type: 3 // 1 公司 2 分公司 3 部门, 用于在组件内控制icon显示
      }
    ];
    treeLoading.value = true;
    treeData.value = handleTree(data);
    treeLoading.value = false;
  });

  return {
    treeData,
    treeLoading,
    form,
    loading,
    columns,
    dataList,
    selectedNum,
    deviceDetection,
    onTreeSelect,
    onSearch,
    resetForm
  };
}
