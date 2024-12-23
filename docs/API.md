# API 文档

## 核心模块

### ViewModel

数据视图模型基类,实现数据绑定。

```python
class ViewModel(QObject):
    """基础ViewModel类,实现数据绑定"""
    dataChanged = Signal()
```

### BaseComponent

可复用的基础组件类。

```python
class BaseComponent(QWidget):
    """可复用的基础组件类"""
    def setupComponent(self):
        """组件初始化"""
        pass
```

## 组件库

### Table

表格组件,支持分页、排序等功能。

### Form

表单组件,支持验证、动态字段等功能。
