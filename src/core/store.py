class Store:
    """全局状态管理"""
    def __init__(self):
        self._state = {}
        self._mutations = {}
        self._actions = {}
        
    def commit(self, mutation, payload=None):
        """同步修改状态"""
        if mutation in self._mutations:
            self._mutations[mutation](self._state, payload)
            
    def dispatch(self, action, payload=None):
        """异步修改状态"""
        if action in self._actions:
            self._actions[action](self, payload) 