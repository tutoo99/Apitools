# PySide6 企业级桌面应用框架

基于 Vue Vben Admin 的设计理念,为 PySide6 定制的企业级应用开发框架。提供了完整的 MVVM 架构实现、组件化支持、主题系统、路由管理等核心功能。

## 特性

- 🎯 基于 MVVM 架构,实现数据驱动的 UI 更新
- 📦 组件化设计,提供丰富的基础组件
- 🎨 主题系统,支持动态切换主题
- 🚦 路由管理,实现页面导航
- 📊 状态管理,处理全局状态
- ✅ 表单验证,统一的验证机制

## 项目结构

```
project/
├── src/
│   ├── core/           # 核心功能模块
│   │   ├── base.py     # 基础类
│   │   ├── components.py # 组件基类
│   │   ├── theme.py    # 主题管理
│   │   ├── router.py   # 路由管理
│   │   └── store.py    # 状态管理
│   ├── components/     # 通用组件
│   │   ├── table.py    # 表格组件
│   │   └── form.py     # 表单组件
│   ├── views/          # 页面视图
│   │   └── user/       # 用户模块
│   │       └── list.py # 用户列表
│   ���── models/         # 数据模型
│   ├── services/       # 业务服务
│   └── utils/          # 工具函数
├── tests/              # 测试文件
├── docs/               # 文档
└── scripts/            # 构建脚本
```

## 快速开始

1. 创建视图模型

```python
from src.core.base import ViewModel

class UserViewModel(ViewModel):
    def __init__(self):
        super().__init__()

    def loadData(self):
        # 加载数据
        data = {
            'users': [
                {'username': 'admin', 'email': 'admin@example.com'}
            ]
        }
        self.setData(data)
```

2. 创建页面视图

```python
from src.core.components import BaseComponent
from src.components.table import Table

class UserListView(BaseComponent):
    def __init__(self):
        super().__init__()
        self.vm = UserViewModel()
        self.setupUI()

    def setupUI(self):
        self.table = Table()
        self.table.columns = [
            {"title": "用户名", "key": "username"},
            {"title": "邮箱", "key": "email"}
        ]
        self.vm.dataChanged.connect(self.onDataChanged)
        self.vm.loadData()
```

## 核心功能

### MVVM 数据绑定

使用 Qt 的信号槽机制实现数据绑定:

```python
class ViewModel(QObject):
    dataChanged = Signal()

    @Property(dict, notify=dataChanged)
    def data(self):
        return self._data
```

### 主题管理

支持动态切换主题:

```python
theme_manager = ThemeManager()
theme_manager.apply_theme('dark')
```

### 路由管理

页面导航管理:

```python
router = Router()
router.register('/user/list', UserListView)
router.push('/user/list', {'id': 1})
```

### 状态管理

全局状态管理:

```python
store = Store()
store.commit('updateUser', {'name': 'admin'})
store.dispatch('fetchUserInfo')
```

## 组件库

### 表格组件

```python
table = Table()
table.columns = [
    {"title": "用户名", "key": "username"},
    {"title": "邮箱", "key": "email"}
]
table.setData(data)
```

### 表单组件

```python
form = Form()
form.addField('username', QLineEdit(), {
    'required': True,
    'min': 3
})
valid, errors = form.validate()
```

## 开发规范

1. 遵循 PEP 8 编码规范
2. 使用类型提示
3. 编写详细的文档字符串
4. 保持代码简洁清晰
5. 编写单元测试

## 最佳实践

1. 组件化开发

   - 将通用功能封装为组件
   - 保持组件的单一职责
   - 提供清晰的组件接口

2. 数据流管理

   - 统一的数据流向
   - 避免组件间直接通信
   - 使用状态管理处理共享数据

3. 性能优化

   - 实现数据懒加载
   - 使用虚拟滚动
   - 优化大数据渲染

4. 错误处理
   - 统一的错误处理机制
   - 友好的错误提示
   - 完善的日志记录

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交代码
4. 创建 Pull Request

## 许可证

[MIT](LICENSE)
