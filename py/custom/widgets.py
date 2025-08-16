from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QFrame, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QIcon, QPainter, QColor, QPixmap

class QtIcon:

    @staticmethod
    def fromTheme(icon_name: str, color: str, size: int = 32) -> QIcon:
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

class AnimatedButton(QPushButton):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._animation = QPropertyAnimation(self, b'')
        self._animation.setDuration(150)
        self._animation.setEasingCurve(QEasingCurve.Type.OutQuad)

    def mousePressEvent(self, event):
        self._animation.stop()
        self._animation.setStartValue(self.geometry())
        self._animation.setEndValue(self.geometry().adjusted(2, 2, -2, -2))
        self._animation.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._animation.stop()
        self._animation.setStartValue(self.geometry())
        self._animation.setEndValue(self.geometry().adjusted(-2, -2, 2, 2))
        self._animation.start()
        super().mouseReleaseEvent(event)

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

    def on_category_changed(self, current):
        if current:
            self.category_selected.emit(current.data(Qt.ItemDataRole.UserRole))
