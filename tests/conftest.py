import pytest
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def app():
    """创建QApplication实例"""
    app = QApplication([])
    yield app
    app.quit() 