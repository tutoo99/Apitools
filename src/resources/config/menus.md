# 菜单配置说明文档

## 配置文件结构

菜单配置使用 JSON 格式，支持多级菜单嵌套。配置文件位于 `src/resources/config/menus.json`。

### 顶层结构

```json
{
  "version": "1.0", // 配置文件版本号
  "menus": [] // 菜单项数组
}
```

### 菜单项属性

每个菜单项支持以下属性：

| 属性名      | 类型     | 必填 | 说明             |
| ----------- | -------- | ---- | ---------------- |
| id          | string   | 是   | 菜单项唯一标识   |
| title       | string   | 是   | 菜单显示名称     |
| icon        | string   | 否   | 菜单图标名称     |
| route       | string   | 否   | 路由路径         |
| permissions | string[] | 否   | 权限配置数组     |
| sort        | number   | 否   | 排序序号(1 开始) |
| children    | array    | 否   | 子菜单数组       |

### 特殊说明

1. `children` 属性用于配置子菜单，支持无限层级嵌套
2. 父级菜单可以不配置 `route`
3. `permissions` 为预留字段，用于后续权限系统集成
4. `sort` 字段决定同级菜单的显示顺序

## 配置示例

```json
{
  "id": "system",
  "title": "系统管理",
  "icon": "settings",
  "sort": 1,
  "children": [
    {
      "id": "users",
      "title": "用户管理",
      "icon": "user",
      "route": "/system/users",
      "permissions": ["manage_users"],
      "sort": 1
    }
  ]
}
```

## 注意事项

1. 确保每个菜单项的 `id` 在整个配置中唯一
2. 建议使用有意义的 `id` 值，方便后续维护
3. 图标名称需要与图标库中的名称保持一致
4. 路由路径应与实际路由配置匹配
