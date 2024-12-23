from PySide6.QtWidgets import QWidget

class BaseComponent(QWidget):
    """可复用的基础组件类"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupComponent()
        
    def setupComponent(self):
        """组件初始化"""
        pass
        
    def updateStyle(self, theme):
        """更新组件样式"""
        pass 