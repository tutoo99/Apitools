from PySide6.QtWidgets import QApplication
from components.layout.main_window import MainWindow

class MainApp:
    def __init__(self):
        self.app = QApplication([])
        self.window = MainWindow()
        
    def run(self):
        """运行应用"""
        self.window.show()
        return self.app.exec()

if __name__ == "__main__":
    app = MainApp()
    app.run() 