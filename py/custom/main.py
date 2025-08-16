import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget
from decorator import QtWindow
from widgets import CategoryMenu, SearchWidget
from service import get_categories

class MainWindow(QtWindow):
    def __init__(self):
        super().__init__()
        self.new_window = None
        self.set_title('主窗体')

        categories = get_categories()
        leftMenu = CategoryMenu(categories)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        search = SearchWidget()
        content_layout.addWidget(search, 2)

        list_widget = QListWidget()
        content_layout.addWidget(list_widget, 8)

        self.main_layout.addWidget(leftMenu, 2)
        self.main_layout.addWidget(content, 8)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
