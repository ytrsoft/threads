import sys
from PyQt6.QtWidgets import QApplication
from decorator import QtWindow
from widgets import CategoryMenu
from service import get_categories

class MainWindow(QtWindow):
    def __init__(self):
        super().__init__()
        self.new_window = None
        self.set_title('主窗体')
        categories = get_categories()
        leftMenu = CategoryMenu(categories)
        rightMenu = CategoryMenu(categories)
        self.main_layout.addWidget(leftMenu, 2)
        self.main_layout.addWidget(rightMenu, 8)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
