from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QFrame, QPushButton, QWidget, QHBoxLayout, QLineEdit
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon, QPainter, QColor, QPixmap

class QtIcon:

    @staticmethod
    def fromTheme(icon_name: str, color: str, size: int = 32):
        base_icon = QIcon.fromTheme(icon_name)
        pixmap = base_icon.pixmap(size, size)
        if pixmap.isNull():
            return base_icon

        colored_pixmap = QPixmap(pixmap.size())
        colored_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(colored_pixmap)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(colored_pixmap.rect(), QColor(color))
        painter.end()

        return QIcon(colored_pixmap)

class CategoryMenu(QListWidget):
    category_selected = pyqtSignal(str)

    def __init__(self, categories, parent=None):
        super().__init__(parent)
        self.categories = categories
        self._setup_ui()
        self.load_categories()

    def _setup_ui(self):
        self.setStyleSheet('''
            QListWidget {
                background: transparent;
                border: none;
                outline: none;
                padding: 8px 0;
            }
            QListWidget::item {
                height: 40px;
                padding-left: 20px;
                border-left: 4px solid transparent;
                color: #B7B9BF;
                font-size: 14px;
 
            }
            QListWidget::item:hover {
                background-color: #2a2a2a;
            }
            QListWidget::item:selected {
                background-color: #333333;
                border-left: 4px solid #4a90e2;
                color: #ffffff;
                font-weight: 500;
            }
            QScrollBar:vertical {
                width: 0px;
                background: transparent;
            }
            QScrollBar::handle:vertical {
                background: transparent;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
                background: transparent;
            }
            QScrollBar::add-page:vertical,
                QScrollBar::sub-page:vertical {
                background: transparent;
            }
      ''')
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.currentItemChanged.connect(self.on_category_changed)

    def load_categories(self):
        self.clear()
        folder_icon = QtIcon.fromTheme('folder', '#B7B9BF')
        all_item = QListWidgetItem(folder_icon, '全部')
        all_item.setData(Qt.ItemDataRole.UserRole, '')
        self.addItem(all_item)

        for category in self.categories:
            item = QListWidgetItem(folder_icon, f'  {category.title}')
            item.setData(Qt.ItemDataRole.UserRole, category.id)
            self.addItem(item)

        self.setCurrentRow(0)

    def on_category_changed(self, current):
        if current:
            self.category_selected.emit(current.data(Qt.ItemDataRole.UserRole))

class SearchWidget(QWidget):
    search_triggered = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setFixedHeight(60)
        self.setStyleSheet("""
            SearchWidget {
                background-color: #2a2a2a;
                border-radius: 8px;
            }
        """)
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        container = QWidget(self)
        container.setStyleSheet("background-color: #333333; border-radius: 8px;")
        
        inner_layout = QHBoxLayout(container)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("请输入关键字...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: none;
                font-size: 14px;
                color: #ffffff;
                background: transparent;
            }
        """)
        self.search_input.returnPressed.connect(self._on_search)
        inner_layout.addWidget(self.search_input)

        self.search_button = QPushButton('搜索')
        self.search_button.setStyleSheet("""
            QPushButton {
                background: #4a90e2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover { background: #3a80d2; }
        """)
        self.search_button.clicked.connect(self._on_search)
        inner_layout.addWidget(self.search_button)
        
        main_layout.addWidget(container)
        self.setLayout(main_layout)

        main_layout.setContentsMargins(0, 6, 0, 0)

    def _on_search(self):
        keyword = self.search_input.text().strip()
        self.search_triggered.emit(keyword)

    def clear_search(self):
        self.search_input.clear()
