import os
import json
import pytest
from src.core.menu_loader import MenuLoader, MenuLoadError

@pytest.fixture
def menu_loader():
    """创建MenuLoader实例"""
    return MenuLoader()

@pytest.fixture
def valid_config(tmp_path):
    """创建有效的测试配置文件"""
    config = {
        "version": "1.0",
        "menus": [
            {
                "id": "test",
                "title": "测试菜单",
                "icon": "test",
                "route": "/test",
                "permissions": ["test"],
                "sort": 1
            }
        ]
    }
    
    config_path = tmp_path / "menus.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f)
        
    return str(config_path)

def test_singleton(menu_loader):
    """测试单例模式"""
    loader1 = MenuLoader()
    loader2 = MenuLoader()
    assert loader1 is loader2

def test_load_valid_config(menu_loader, valid_config, monkeypatch):
    """测试加载有效配置"""
    # 修改配置文件路径
    monkeypatch.setattr(menu_loader, '_config_path', valid_config)
    
    # 监听信号
    loaded_config = None
    def on_loaded(config):
        nonlocal loaded_config
        loaded_config = config
    menu_loader.menu_loaded.connect(on_loaded)
    
    # 加载配置
    menu_loader.load_config()
    
    assert loaded_config is not None
    assert len(loaded_config) == 1
    assert loaded_config[0]['id'] == 'test'

def test_load_nonexistent_file(menu_loader):
    """测试加载不存在的文件"""
    menu_loader._config_path = 'nonexistent.json'
    
    with pytest.raises(MenuLoadError) as exc_info:
        menu_loader.load_config()
    assert "配置文件不存在" in str(exc_info.value)

def test_load_invalid_json(menu_loader, tmp_path):
    """测试加载无效的JSON"""
    # 创建无效的JSON文件
    config_path = tmp_path / "invalid.json"
    with open(config_path, 'w') as f:
        f.write("{invalid json")
    
    menu_loader._config_path = str(config_path)
    
    with pytest.raises(MenuLoadError) as exc_info:
        menu_loader.load_config()
    assert "JSON格式错误" in str(exc_info.value)

def test_validate_missing_required_fields(menu_loader):
    """测试缺少必填字段"""
    invalid_config = {
        "version": "1.0",
        "menus": [
            {
                "title": "���试菜单"  # 缺少id
            }
        ]
    }
    
    with pytest.raises(MenuLoadError) as exc_info:
        menu_loader._validate_config(invalid_config)
    assert "缺少id字段" in str(exc_info.value)

def test_validate_invalid_field_types(menu_loader):
    """测试字段类型错误"""
    invalid_config = {
        "version": "1.0",
        "menus": [
            {
                "id": 123,  # id应该是字符串
                "title": "测试菜单"
            }
        ]
    }
    
    with pytest.raises(MenuLoadError) as exc_info:
        menu_loader._validate_config(invalid_config)
    assert "id必须是字符串" in str(exc_info.value)

def test_validate_nested_menus(menu_loader):
    """测试嵌套菜单验证"""
    config = {
        "version": "1.0",
        "menus": [
            {
                "id": "parent",
                "title": "父菜单",
                "children": [
                    {
                        "id": "child",
                        "title": "子菜单"
                    }
                ]
            }
        ]
    }
    
    # 不应该抛出异常
    menu_loader._validate_config(config) 