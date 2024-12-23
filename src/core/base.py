from PySide6.QtCore import QObject, Signal, Property

class ViewModel(QObject):
    """基础ViewModel类,实现数据绑定"""
    dataChanged = Signal()  # 数据变更信号
    
    def __init__(self):
        super().__init__()
        self._data = {}
        
    @Property(dict, notify=dataChanged)
    def data(self):
        return self._data
        
    def setData(self, value):
        self._data = value
        self.dataChanged.emit() 