import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from decorator import QtWindow

class MainWindow(QtWindow):
    def __init__(self):
        super().__init__()
        self.new_window = None
        self.set_title("主窗口")
        btn = QPushButton("跳转")
        btn.setFixedSize(160, 40)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        btn.clicked.connect(self.open_new_window)
        self.main_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def open_new_window(self):
        self.new_window = SubWindow(self)
        self.new_window.show()
        self.hide()

class SubWindow(QtWindow):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.set_title("新窗口")
        back_btn = QPushButton("返回")
        back_btn.setFixedSize(160, 40)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        back_btn.clicked.connect(self.go_back)
        layout = QVBoxLayout(self.main_widget)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def go_back(self):
        self.parent_window.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
