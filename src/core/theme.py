from PySide6.QtCore import QObject, Signal
from enum import Enum

class Theme(Enum):
    LIGHT = "light"
    DARK = "dark"
    ORANGE = "orange"

class ThemeManager(QObject):
    """主题管理器"""
    themeChanged = Signal(Theme)  # 主题变更信号
    
    def __init__(self):
        super().__init__()
        self._current_theme = Theme.ORANGE
        self._themes = {
            Theme.LIGHT: {
                "primary": "#1890FF",
                "background": "#FFFFFF",
                "sidebar": "#FFFFFF",
                "header": "#FFFFFF",
                "text": "#333333",
                "border": "#E8E8E8"
            },
            Theme.DARK: {
                "primary": "#1890FF",
                "background": "#1E1E1E",
                "sidebar": "#252526",
                "header": "#252526",
                "text": "#FFFFFF",
                "border": "#333333"
            },
            Theme.ORANGE: {
                "primary": "#FF8C00",
                "background": "#FFFFFF",
                "sidebar": "#FF8C00",
                "header": "#FF8C00",
                "text": "#FFFFFF",
                "border": "#FF9932"
            }
        }
    
    def get_theme(self) -> Theme:
        """获取当前主题"""
        return self._current_theme
    
    def set_theme(self, theme: Theme):
        """设置主题"""
        if theme != self._current_theme:
            self._current_theme = theme
            self.themeChanged.emit(theme)
    
    def get_style(self) -> dict:
        """获取当前主题样式"""
        return self._themes[self._current_theme]
    
    def get_theme_style(self, theme: Theme) -> dict:
        """获取指定主题样式"""
        return self._themes[theme]