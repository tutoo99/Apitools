class Router:
    """视图路由管理"""
    def __init__(self):
        self.routes = {}
        self.current = None
        
    def register(self, path, view_class):
        """注册路由"""
        self.routes[path] = view_class
        
    def push(self, path, params=None):
        """路由跳转"""
        if path in self.routes:
            view = self.routes[path]()
            if params:
                view.setParams(params)
            self.current = view
            return view 