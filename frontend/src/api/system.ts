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

export type Group = {
  id: number;
  name: string;
};

// permissions数据列表type
export type PermissionResult = {
  success: boolean;
  data: [
    {
      id: number;
      content_type_id: number;
      name: string;
      codename: string;
    }
  ];
  msg: string;
};

// group数据列表type
export type Permission = {
  id: number;
  content_type_id: number;
  name: string;
  codename: string;
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

// permission接口
export const getPermissions = () => {
  return http.request<PermissionResult>("get", "api/system/permissions/");
};

export const putPermissions = (id?: number, data?: object) => {
  return http.request<Permission>("put", "api/system/permissions/" + id + "/", { data });
};
