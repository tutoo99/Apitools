from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import Signal, Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon, QColor
from pathlib import Path
from core.theme import ThemeManager, Theme

class MenuItem(QWidget):
    """菜单项组件"""
    clicked = Signal(str)  # 菜单点击信号
    
    def __init__(self, text, route, icon=None, parent=None):
        super().__init__(parent)
        self.route = route
        self.is_expanded = False
        self.sub_items = []
        
        # 获取父组件的主题管理器
        self.theme_manager = self.get_theme_manager()
        if self.theme_manager:
            self.theme_manager.themeChanged.connect(self._on_theme_changed)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 主按钮容器
        self.btn_container = QWidget()
        btn_layout = QHBoxLayout(self.btn_container)
        btn_layout.setContentsMargins(16, 0, 16, 0)
        btn_layout.setSpacing(8)
        
        # 图标
        self.icon_label = QLabel()
        if icon:
            icon_path = str(Path(__file__).parent.parent.parent / "resources" / "icons" / icon)
            self.icon_label.setPixmap(QIcon(icon_path).pixmap(16, 16))
        btn_layout.addWidget(self.icon_label)
        
        # 文本
        self.text_label = QLabel(text)
        btn_layout.addWidget(self.text_label)
        
        # 箭头图标
        self.arrow_label = QLabel("▸")
        self.arrow_label.setVisible(False)
        btn_layout.addWidget(self.arrow_label)
        
        btn_layout.addStretch()
        layout.addWidget(self.btn_container)
        
        # 点击效果
        self.btn_container.setCursor(Qt.PointingHandCursor)
        self.btn_container.mousePressEvent = self._on_pressed
        self.btn_container.mouseReleaseEvent = self._on_released
        self.btn_container.enterEvent = self._on_enter
        self.btn_container.leaveEvent = self._on_leave
        
        # 子菜单容器
        self.sub_menu = QWidget()
        self.sub_menu.setVisible(False)
        self.sub_menu.setMaximumHeight(0)
        self.sub_layout = QVBoxLayout(self.sub_menu)
        self.sub_layout.setContentsMargins(0, 0, 0, 0)
        self.sub_layout.setSpacing(0)
        layout.addWidget(self.sub_menu)
        
        # 动画
        self.animation = QPropertyAnimation(self.sub_menu, b"maximumHeight")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        
        # 箭头动画
        self.arrow_animation = QPropertyAnimation(self.arrow_label, b"rotation")
        self.arrow_animation.setDuration(200)
        self.arrow_animation.setEasingCurve(QEasingCurve.InOutCubic)
        
        # 应用初始主题
        if self.theme_manager:
            self._apply_theme(self.theme_manager.get_theme())
        
    def get_theme_manager(self):
        """获取主题管理器"""
        parent = self.parent()
        while parent:
            if hasattr(parent, 'theme_manager'):
                return parent.theme_manager
            parent = parent.parent()
        return None
        
    def add_sub_item(self, text, route, icon=None):
        """添加子菜单"""
        if not self.arrow_label.isVisible():
            self.arrow_label.setVisible(True)
        
        # 创建子菜单容器
        sub_item_container = QWidget()
        sub_item_layout = QHBoxLayout(sub_item_container)
        sub_item_layout.setContentsMargins(20, 0, 0, 0)  # 左侧添加20px的缩进
        sub_item_layout.setSpacing(0)
        
        # 创建子菜单项
        sub_item = MenuItem(text, route, icon, self)
        sub_item.clicked.connect(self.clicked)
        sub_item_layout.addWidget(sub_item)
        
        self.sub_items.append(sub_item)
        self.sub_layout.addWidget(sub_item_container)
        
        # 更新子菜单最大高度
        total_height = sum(item.sizeHint().height() for item in self.sub_items)
        self.animation.setEndValue(total_height)
        
        return sub_item
        
    def _on_pressed(self, event):
        """按下效果"""
        if self.theme_manager:
            style = self.theme_manager.get_style()
            self.btn_container.setStyleSheet(f"""
                QWidget {{
                    background-color: {style['primary']};
                    border-radius: 4px;
                    margin: 2px 8px;
                }}
            """)
        
    def _on_released(self, event):
        """释放效果"""
        if self.theme_manager:
            style = self.theme_manager.get_style()
            self.btn_container.setStyleSheet(f"""
                QWidget {{
                    background-color: {style['sidebar']};
                    border-radius: 4px;
                    margin: 2px 8px;
                }}
                QWidget:hover {{
                    background-color: {style['primary']};
                }}
            """)
        self._on_clicked()
        
    def _on_enter(self, event):
        """鼠标进入效果"""
        if self.theme_manager:
            style = self.theme_manager.get_style()
            self.btn_container.setStyleSheet(f"""
                QWidget {{
                    background-color: {style['primary']};
                    border-radius: 4px;
                    margin: 2px 8px;
                }}
            """)
        
    def _on_leave(self, event):
        """鼠标离开效果"""
        if self.theme_manager:
            style = self.theme_manager.get_style()
            self.btn_container.setStyleSheet(f"""
                QWidget {{
                    background-color: {style['sidebar']};
                    border-radius: 4px;
                    margin: 2px 8px;
                }}
                QWidget:hover {{
                    background-color: {style['primary']};
                }}
            """)
        
    def _on_clicked(self):
        """点击处理"""
        if self.sub_items:
            self.is_expanded = not self.is_expanded
            
            # 子菜单展开/收起动画
            if self.is_expanded:
                self.sub_menu.setVisible(True)
                self.animation.setStartValue(0)
                self.animation.setEndValue(self.sub_layout.sizeHint().height())
                self.arrow_animation.setStartValue(0)
                self.arrow_animation.setEndValue(90)
                
                # 设置展开状态的样式
                if self.theme_manager:
                    style = self.theme_manager.get_style()
                    self.btn_container.setStyleSheet(f"""
                        QWidget {{
                            background-color: {style['primary']};
                            border-radius: 4px;
                            margin: 2px 8px;
                        }}
                    """)
            else:
                self.animation.setStartValue(self.sub_menu.height())
                self.animation.setEndValue(0)
                self.arrow_animation.setStartValue(90)
                self.arrow_animation.setEndValue(0)
                
                # 恢复默认样式
                if self.theme_manager:
                    style = self.theme_manager.get_style()
                    self.btn_container.setStyleSheet(f"""
                        QWidget {{
                            background-color: {style['sidebar']};
                            border-radius: 4px;
                            margin: 2px 8px;
                        }}
                        QWidget:hover {{
                            background-color: {style['primary']};
                        }}
                    """)
            
            self.animation.start()
            self.arrow_animation.start()
            
            if not self.is_expanded:
                self.animation.finished.connect(
                    lambda: self.sub_menu.setVisible(False))
        
        # 无论是否有子菜单，都发送点击信号
        if self.route:
            self.clicked.emit(self.route)
        
    def collapse(self):
        """收起菜单项"""
        self.text_label.setVisible(False)
        self.arrow_label.setVisible(False)
        self.btn_container.setFixedWidth(48)
        
    def expand(self):
        """展开菜单项"""
        self.text_label.setVisible(True)
        self.arrow_label.setVisible(len(self.sub_items) > 0)
        self.btn_container.setFixedWidth(200)
        
    def _on_theme_changed(self, theme: Theme):
        """主题变更处理"""
        self._apply_theme(theme)
        
    def _apply_theme(self, theme: Theme):
        """应用主题"""
        if not self.theme_manager:
            return
            
        style = self.theme_manager.get_theme_style(theme)
        
        # 设置整个菜单项的背景色
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {style['sidebar']};
            }}
        """)
        
        # 设置文本颜色
        self.text_label.setStyleSheet(f"""
            QLabel {{
                color: {style['text']};
                font-size: 14px;
                font-weight: 500;
            }}
        """)
        
        # 设置箭头颜色
        self.arrow_label.setStyleSheet(f"""
            QLabel {{
                color: {style['text']};
                font-size: 12px;
            }}
        """)
        
        # 设置按钮容器的悬停效果
        self.btn_container.setStyleSheet(f"""
            QWidget {{
                background-color: {style['sidebar']};
                border-radius: 4px;
                margin: 2px 8px;
            }}
            QWidget:hover {{
                background-color: {style['primary']};
            }}
        """)
        
        # 设置子菜单容器的样式
        self.sub_menu.setStyleSheet(f"""
            QWidget {{
                background-color: {style['sidebar']};
            }}
            QWidget > QWidget {{  /* 子菜单项容器 */
                background-color: {style['sidebar']};
                margin-left: 0;
            }}
        """)