import { http } from "@/utils/http";
// depart数据列表type
export type DepartResult = {
  success: boolean;
  data: [];
  msg: string;
};

export type Depart = {
  id: string;
  name: string;
  code: string;
  rank: number;
  type: number;
  parent: string;
  status: boolean;
  roles: [];
};

export type newDepartResult = {
  success: boolean;
  data: object;
  msg: string;
};

/** 获取部门数据列表 */
export const getDepartList = (params?: object) => {
  return http.request<DepartResult>("get", "/api/system/dept/", { params });
};

/** 新增部门 */
export const postDepart = (data?: object) => {
  return http.request<newDepartResult>("post", "/api/system/dept/", { data });
};

/** 删除部门 */
export const deleteDepart = (id?: number) => {
  return http.request<newDepartResult>("delete", "/api/system/dept/" + id + "/");
};

/** 部分更新部门数据 */
export const patchDepart = (id?: number, data?: object) => {
  return http.request<newDepartResult>("patch", "/api/system/dept/" + id + "/", { data });
};
