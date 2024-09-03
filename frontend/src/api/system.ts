import { http } from "@/utils/http";

// group数据列表type
export type GroupResult = {
  success: boolean;
  data: [
    {
      id: number;
      name: string;
    }
  ];
  msg: string;
};

// group数据列表type
export type Group = {
  name: string;
};

// group接口
export const getGroups = () => {
  return http.request<GroupResult>("get", "api/system/groups/");
};

export const postGroup = (data?: object) => {
  return http.request<Group>("post", "api/system/groups/", { data });
};

export const deletGroup = (id?: number) => {
  return http.request("delete", "api/system/groups/" + id + "/");
};
