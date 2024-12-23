from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from core.theme import ThemeManager, Theme

class Content(QStackedWidget):
    """内容区"""
    def __init__(self, theme_manager):
        super().__init__()
        self.theme_manager = theme_manager
        self.theme_manager.themeChanged.connect(self._on_theme_changed)
        self.setObjectName("content")
        
        # 创建开发中页面
        self.developing = QWidget()
        self.developing.setObjectName("developing")
        layout = QVBoxLayout(self.developing)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setAlignment(Qt.AlignCenter)
        
        # 创建提示容器
        tip_container = QWidget()
        tip_container.setObjectName("developing_message")
        tip_layout = QVBoxLayout(tip_container)
        tip_layout.setContentsMargins(40, 40, 40, 40)
        
        # 标题
        self.title_label = QLabel("仪表盘")
        self.title_label.setObjectName("title")
        tip_layout.addWidget(self.title_label, 0, Qt.AlignCenter)
        
        # 提示信息
        self.message = QLabel("正在开发中，小主你先歇一会儿...")
        self.message.setObjectName("message")
        tip_layout.addWidget(self.message, 0, Qt.AlignCenter)
        
        layout.addWidget(tip_container)
        self.addWidget(self.developing)
        
        # 应用初始主题
        self._apply_theme(self.theme_manager.get_theme())
        
    def show_route(self, route, title):
        """显示路由对应的内容"""
        self.title_label.setText(title)
        self.message.setText("正在开发中，小主你先歇一会儿...")
        self.setCurrentWidget(self.developing)
        
    def _on_theme_changed(self, theme: Theme):
        """主题变更处理"""
        self._apply_theme(theme)
        
    def _apply_theme(self, theme: Theme):
        """应用主题"""
        style = self.theme_manager.get_theme_style(theme)
        self.setStyleSheet(f"""
            #content {{
                background-color: {style['background']};
                padding: 20px;
            }}
            
            #developing {{
                background-color: {style['background']};
            }}
            
            #developing_message {{
                background-color: {style['background']};
                border: 2px solid {style['primary']};
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                min-width: 400px;
                max-width: 600px;
            }}
            
            #title {{
                color: {style['text']};
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 16px;
            }}
            
            #message {{
                color: {style['text']};
                font-size: 16px;
                opacity: 0.8;
            }}
        """)
        