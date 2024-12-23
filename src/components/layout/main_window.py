from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                              QStackedWidget, QToolButton, QMenu)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QResizeEvent
from .sidebar import Sidebar
from .header import Header
from .content import Content
from core.theme import ThemeManager, Theme

class MainWindow(QMainWindow):
    """主窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 企业级中后台")
        self.resize(1200, 800)
        
        # 初始化主题管理器
        self.theme_manager = ThemeManager()
        self.theme_manager.themeChanged.connect(self._on_theme_changed)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 创建侧边栏
        self.sidebar = Sidebar(self.theme_manager)
        self.sidebar.menuClicked.connect(self._on_menu_clicked)
        self.main_layout.addWidget(self.sidebar)
        
        # 创建右侧内容区
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        
        # 创建顶部导航
        self.header = Header(self.theme_manager)
        right_layout.addWidget(self.header)
        
        # 创建内容区
        self.content = Content(self.theme_manager)
        right_layout.addWidget(self.content)
        
        self.main_layout.addWidget(right_container)
        
        # 设置布局比例
        self.main_layout.setStretch(0, 0)  # 侧边栏固定宽度
        self.main_layout.setStretch(1, 1)  # 内容区自适应
        
        # 添加主题切换按钮
        self._setup_theme_button()
        
        # 应用初始主题
        self._apply_theme(self.theme_manager.get_theme())
        
    def _setup_theme_button(self):
        """设置主题切换按钮"""
        theme_btn = QToolButton(self.header)
        theme_btn.setPopupMode(QToolButton.InstantPopup)
        theme_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        theme_btn.setText("主题")
        theme_btn.setStyleSheet("""
            QToolButton {
                color: #FFFFFF;
                border: none;
                padding: 4px 8px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
            }
            QToolButton:hover {
                background: rgba(255, 255, 255, 0.2);
            }
            QMenu {
                background-color: #FFFFFF;
                border: 1px solid #E8E8E8;
                border-radius: 4px;
                padding: 4px 0;
            }
            QMenu::item {
                padding: 8px 24px;
            }
            QMenu::item:selected {
                background-color: #F5F5F5;
            }
        """)
        
        # 创建主题菜单
        theme_menu = QMenu(theme_btn)
        themes = {
            "橙色主题": Theme.ORANGE,
            "亮色主题": Theme.LIGHT,
            "暗色主题": Theme.DARK
        }
        for name, theme in themes.items():
            action = theme_menu.addAction(name)
            action.triggered.connect(lambda checked, t=theme: self.theme_manager.set_theme(t))
        
        theme_btn.setMenu(theme_menu)
        self.header.layout().insertWidget(self.header.layout().count()-1, theme_btn)
        
    def _on_theme_changed(self, theme: Theme):
        """主题变更处理"""
        self._apply_theme(theme)
        
    def _apply_theme(self, theme: Theme):
        """应用主题"""
        style = self.theme_manager.get_theme_style(theme)
        
        # 更新窗口样式
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {style['background']};
            }}
            QWidget {{
                font-family: "Microsoft YaHei", "Segoe UI", "Helvetica Neue";
            }}
        """)
        
    def resizeEvent(self, event: QResizeEvent):
        """窗口大小变更处理"""
        super().resizeEvent(event)
        width = event.size().width()
        
        # 响应式布局处理
        if width < 768:  # 移动端
            self.sidebar.setMaximumWidth(0)
            self.sidebar.setVisible(False)
        elif width < 992:  # 平板
            self.sidebar.setMaximumWidth(64)
            self.sidebar.setVisible(True)
            self.sidebar.collapse()
        else:  # 桌面端
            self.sidebar.setMaximumWidth(220)
            self.sidebar.setVisible(True)
            self.sidebar.expand()
        
    def _on_menu_clicked(self, route, title):
        """菜单点击处理"""
        self.header.update_breadcrumb(title)
        self.content.show_route(route, title)