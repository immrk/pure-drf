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

export type Role = {
  id: number;
  name: string;
  code: string;
  status: boolean;
  parent: string;
  create_time: string;
  update_time: string;
};

export type RolesResult = {
  success: boolean;
  data: [];
  msg: string;
};

export type NewRoleResult = {
  success: boolean;
  data: Role;
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

/** 获取角色数据列表 */
export const getRoleList = (params?: object) => {
  return http.request<RolesResult>("get", "/api/system/role/", { params });
};

/** 新增角色 */
export const postRole = (data?: object) => {
  return http.request<NewRoleResult>("post", "/api/system/role/", { data });
};

/** 删除角色 */
export const deleteRole = (id?: number) => {
  return http.request<NewRoleResult>("delete", "/api/system/role/" + id + "/");
};

/** 部分更新角色数据 */
export const patchRole = (id?: number, data?: object) => {
  return http.request<NewRoleResult>("patch", "/api/system/role/" + id + "/", { data });
};
