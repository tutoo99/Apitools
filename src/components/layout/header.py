from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from core.theme import ThemeManager, Theme

class Header(QWidget):
    """顶部导航"""
    def __init__(self, theme_manager):
        super().__init__()
        self.theme_manager = theme_manager
        self.theme_manager.themeChanged.connect(self._on_theme_changed)
        self.setObjectName("header")
        self._apply_theme(self.theme_manager.get_theme())
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # 面包屑导航
        self.breadcrumb = QLabel("首页")
        layout.addWidget(self.breadcrumb)
        
        layout.addStretch()
        
        # 用户信息
        self.user_info = QLabel("Admin")
        layout.addWidget(self.user_info)
        
        # 设置对象名以应用特定样式
        self.breadcrumb.setObjectName("breadcrumb")
        self.user_info.setObjectName("user_info")
        
        # 添加鼠标样式
        self.breadcrumb.setCursor(Qt.PointingHandCursor)
        self.user_info.setCursor(Qt.PointingHandCursor)
        
    def update_breadcrumb(self, title):
        """更新面包屑"""
        self.breadcrumb.setText(title)
        
    def _on_theme_changed(self, theme: Theme):
        """主题变更处理"""
        self._apply_theme(theme)
        
    def _apply_theme(self, theme: Theme):
        """应用主题"""
        style = self.theme_manager.get_theme_style(theme)
        self.setStyleSheet(f"""
            #header {{
                background-color: {style['header']};
                border-bottom: 1px solid {style['border']};
                min-height: 48px;
            }}
            QLabel {{
                color: {style['text']};
                font-size: 14px;
                font-weight: 500;
            }}
            #breadcrumb {{
                padding: 0 8px;
                border-radius: 4px;
            }}
            #breadcrumb:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
            #user_info {{
                padding: 6px 12px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
            }}
            #user_info:hover {{
                background: rgba(255, 255, 255, 0.2);
            }}
        """)