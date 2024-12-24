import json
import os
from typing import Dict, List, Optional
from PySide6.QtCore import QObject, Signal

class MenuLoadError(Exception):
    """菜单加载错误异常类"""
    pass

class MenuLoader(QObject):
    """菜单配置加载器
    
    使用单例模式确保全局只有一个实例
    继承QObject以支持信号机制
    """
    
    # 定义信号
    menu_loaded = Signal(list)  # 菜单加载完成信号
    load_error = Signal(str)    # 加载错误信号
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MenuLoader, cls).__new__(cls)
        return cls._instance
        
    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self._initialized = True
            self._menu_config = None
            self._config_path = os.path.join('src', 'resources', 'config', 'menus.json')
    
    @property
    def menu_config(self) -> Optional[List[Dict]]:
        """获取当前加载的菜单配置"""
        return self._menu_config
        
    def load_config(self) -> None:
        """加载菜单配置
        
        从配置文件加载菜单配置,进行验证后发出相应信号
        如果加载失败,发出错误信号
        """
        try:
            if not os.path.exists(self._config_path):
                raise MenuLoadError(f"配置文件不存在: {self._config_path}")
                
            with open(self._config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            # 验证配置格式
            self._validate_config(config)
            
            # 更新配置并发出信号
            self._menu_config = config['menus']
            self.menu_loaded.emit(self._menu_config)
            
        except json.JSONDecodeError as e:
            error_msg = f"JSON格式错误: {str(e)}"
            self.load_error.emit(error_msg)
            raise MenuLoadError(error_msg)
            
        except Exception as e:
            error_msg = f"加载配置失败: {str(e)}"
            self.load_error.emit(error_msg)
            raise MenuLoadError(error_msg)
    
    def _validate_config(self, config: Dict) -> None:
        """验证配置格式是否正确
        
        Args:
            config: 要验证的配置字典
            
        Raises:
            MenuLoadError: 当配置���式不正确时抛出
        """
        # 验证顶层结构
        if not isinstance(config, dict):
            raise MenuLoadError("配置必须是一个对象")
            
        if 'version' not in config:
            raise MenuLoadError("缺少version字段")
            
        if 'menus' not in config:
            raise MenuLoadError("缺少menus字段")
            
        if not isinstance(config['menus'], list):
            raise MenuLoadError("menus必须是一个数组")
            
        # 递归验证每个菜单项
        for menu in config['menus']:
            self._validate_menu_item(menu)
    
    def _validate_menu_item(self, item: Dict, parent_id: str = '') -> None:
        """递归验证菜单项
        
        Args:
            item: 要验证的菜单项
            parent_id: 父菜单ID,用于错误提示
            
        Raises:
            MenuLoadError: 当菜单项格式不正确时抛出
        """
        # 验证必填字段
        if 'id' not in item:
            raise MenuLoadError(f"菜单项缺少id字段: {parent_id}")
            
        if 'title' not in item:
            raise MenuLoadError(f"菜单项缺少title字段: {item['id']}")
            
        # 验证字段类型
        if not isinstance(item['id'], str):
            raise MenuLoadError(f"id必须是字符串: {item['id']}")
            
        if not isinstance(item['title'], str):
            raise MenuLoadError(f"title必须是字符串: {item['id']}")
            
        if 'icon' in item and not isinstance(item['icon'], str):
            raise MenuLoadError(f"icon必须是字符串: {item['id']}")
            
        if 'route' in item and not isinstance(item['route'], str):
            raise MenuLoadError(f"route必须是字符串: {item['id']}")
            
        if 'permissions' in item and not isinstance(item['permissions'], list):
            raise MenuLoadError(f"permissions必须是数组: {item['id']}")
            
        if 'sort' in item and not isinstance(item['sort'], (int, float)):
            raise MenuLoadError(f"sort必须是数字: {item['id']}")
            
        # 递归验证子菜单
        if 'children' in item:
            if not isinstance(item['children'], list):
                raise MenuLoadError(f"children必须是数组: {item['id']}")
                
            for child in item['children']:
                self._validate_menu_item(child, item['id']) 