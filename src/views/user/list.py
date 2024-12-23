from PySide6.QtWidgets import QVBoxLayout
from core.components import BaseComponent
from components.table import Table
from .viewmodel import UserViewModel

class UserListView(BaseComponent):
    """用户列表页面"""
    def __init__(self):
        super().__init__()
        self.vm = UserViewModel()
        self.setupUI()
        
    def setupUI(self):
        """初始化UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 创建表格
        self.table = Table()
        self.table.columns = [
            {"title": "用户名", "key": "username"},
            {"title": "邮箱", "key": "email"}
        ]
        layout.addWidget(self.table)
        
        # 绑定数据
        self.vm.dataChanged.connect(self.onDataChanged)
        
        # 加载数据
        self.vm.loadData()
        
    def onDataChanged(self):
        """数据变更处理"""
        self.table.setData(self.vm.data['users'])