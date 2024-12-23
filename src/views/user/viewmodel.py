from core.base import ViewModel

class UserViewModel(ViewModel):
    def __init__(self):
        super().__init__()
        
    def loadData(self):
        """加载用户数据"""
        # 模拟数据
        data = {
            'users': [
                {'username': 'admin', 'email': 'admin@example.com'},
                {'username': 'user1', 'email': 'user1@example.com'},
                {'username': 'user2', 'email': 'user2@example.com'},
            ]
        }
        self.setData(data) 