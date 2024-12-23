from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Signal
from .menu_item import MenuItem
from core.theme import ThemeManager, Theme

class Sidebar(QWidget):
    """侧边栏"""
    menuClicked = Signal(str, str)  # 菜单点击信号(route, title)
    
    def __init__(self, theme_manager):
        super().__init__()
        self.theme_manager = theme_manager
        self.theme_manager.themeChanged.connect(self._on_theme_changed)
        self.is_collapsed = False
        self.setObjectName("sidebar")
        self._apply_theme(self.theme_manager.get_theme())
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo
        logo = QLabel("PySide6 Admin")
        logo.setObjectName("logo")
        layout.addWidget(logo)
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        # 菜单容器
        menu_container = QWidget()
        menu_container.setObjectName("menu_container")
        menu_layout = QVBoxLayout(menu_container)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(0)
        
        # 添加菜单项
        dashboard = MenuItem("仪表盘", "/dashboard", "icons/dashboard.png")
        dashboard.clicked.connect(self._on_menu_clicked)
        menu_layout.addWidget(dashboard)
        
        # 系统管理
        system = MenuItem("系统管理", "", "icons/system.png")
        system.add_sub_item("用户管理", "/system/user")
        system.add_sub_item("角色管理", "/system/role")
        system.add_sub_item("菜单管理", "/system/menu")
        system.clicked.connect(self._on_menu_clicked)
        menu_layout.addWidget(system)
        
        # 内容管理
        content = MenuItem("内容管理", "", "icons/content.png")
        content.add_sub_item("文章管理", "/content/article")
        content.add_sub_item("分类管理", "/content/category")
        content.add_sub_item("标签管理", "/content/tag")
        content.clicked.connect(self._on_menu_clicked)
        menu_layout.addWidget(content)
        
        menu_layout.addStretch()
        scroll.setWidget(menu_container)
        layout.addWidget(scroll)
        
    def _on_menu_clicked(self, route):
        """菜单点击处理"""
        # 根据路由获取题
        titles = {
            "/dashboard": "仪表盘",
            "/system/user": "用户管理",
            "/system/role": "角色管理",
            "/system/menu": "菜单管理",
            "/content/article": "文章管理",
            "/content/category": "分类管理",
            "/content/tag": "标签管理"
        }
        self.menuClicked.emit(route, titles.get(route, ""))
        
    def collapse(self):
        """收起侧边栏"""
        if not self.is_collapsed:
            self.is_collapsed = True
            self.setMaximumWidth(64)
            for item in self.findChildren(MenuItem):
                item.collapse()
                
    def expand(self):
        """展开侧边栏"""
        if self.is_collapsed:
            self.is_collapsed = False
            self.setMaximumWidth(220)
            for item in self.findChildren(MenuItem):
                item.expand()
                
    def _on_theme_changed(self, theme: Theme):
        """主题变更处理"""
        self._apply_theme(theme)
        
    def _apply_theme(self, theme: Theme):
        """应用主题"""
        style = self.theme_manager.get_theme_style(theme)
        self.setStyleSheet(f"""
            /* 侧边栏基础��式 */
            #sidebar {{
                background-color: {style['sidebar']};
                min-width: {64 if self.is_collapsed else 220}px;
                max-width: {64 if self.is_collapsed else 220}px;
                border-right: 1px solid {style['border']};
            }}
            
            /* 滚动区域样式 */
            QScrollArea {{
                border: none;
                background-color: {style['sidebar']};
            }}
            QScrollArea > QWidget > QWidget {{
                background-color: {style['sidebar']};
            }}
            QScrollBar:vertical {{
                width: 8px;
                background: transparent;
                margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: rgba(255, 255, 255, 0.3);
                min-height: 30px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: rgba(255, 255, 255, 0.5);
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0;
            }}
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {{
                background: transparent;
            }}
            
            /* Logo样式 */
            QLabel#logo {{
                color: {style['text']};
                font-size: 20px;
                font-weight: bold;
                padding: 16px 20px;
                background-color: {style['sidebar']};
                border-bottom: 1px solid {style['border']};
            }}
            
            /* 菜单容器样式 */
            QWidget#menu_container {{
                background-color: {style['sidebar']};
            }}
        """)