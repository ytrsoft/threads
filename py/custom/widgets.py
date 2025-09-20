from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QFrame, QPushButton, QWidget, QHBoxLayout, QLineEdit, QVBoxLayout, QSizePolicy, QLabel, QGraphicsDropShadowEffect, QScrollArea
from PyQt6.QtCore import pyqtSignal, Qt, QTimer, QEasingCurve, QPropertyAnimation
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

class PostList(QWidget):
    page_change = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.page = 1
        self.has_more = True
        self.loading = False

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.on_scroll)
        self.layout.addWidget(self.scroll_area)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_layout.setSpacing(12)
        self.scroll_layout.addStretch()
        self.scroll_area.setWidget(self.scroll_content)

        self.refresh()

    def set_posts(self, posts, has_more=True):
        if self.page == 1:
            for i in reversed(range(self.scroll_layout.count())):
                widget = self.scroll_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

        for post in posts:
            card = PostCard(post)
            card.clicked.connect(self.show_post_detail)
            self.scroll_layout.addWidget(card)

        self.has_more = has_more
        self.loading = False
        self.page += 1

    def refresh(self):
        self.page = 1
        self.has_more = True
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        QTimer.singleShot(0, lambda: self.page_change.emit(self.page))

    def on_scroll(self, value):
        scroll_bar = self.scroll_area.verticalScrollBar()
        if not self.loading and self.has_more and value >= scroll_bar.maximum() - 16:
            self.loading = True
            self.page_change.emit(self.page)

    def show_post_detail(self, post_id):
        print(f"Post clicked: {post_id}")
class PostCard(QFrame):
    clicked = pyqtSignal(str)

    def __init__(self, post, parent=None):
        super().__init__(parent)
        self.post = post
        self.setup_ui()
        self.setup_animation()

    def setup_animation(self):
        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setBlurRadius(15)
        self.effect.setColor(QColor(0, 0, 0, 80))
        self.effect.setOffset(0, 3)
        self.setGraphicsEffect(self.effect)

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)

    def setup_ui(self):
        self.setStyleSheet("""
            PostCard {
                background: #2a2a2a;
                border-radius: 10px;
                border: 1px solid #3a3a3a;
            }
            PostCard:hover {
                background: #333333;
                border-color: #4a4a4a;
            }
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(180)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title_label = QLabel(self.post.title)
        title_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #ffffff;")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(8)

        for text, icon in [
            (self.post.region, "📍"),
            (self.post.age, "👧"),
            (self.post.score, "⭐"),
            (self.post.price, "💰")
        ]:
            if text:
                label = QLabel(f"{icon} {text}")
                label.setStyleSheet("""
                    font-size: 13px;
                    color: #b0b0b0;
                    padding: 4px 8px;
                    background: #333333;
                    border-radius: 6px;
                """)
                meta_layout.addWidget(label)

        meta_layout.addStretch()
        layout.addLayout(meta_layout)

        if self.post.desc:
            desc = (self.post.desc[:120] + '...') if len(self.post.desc) > 120 else self.post.desc
            desc_label = QLabel(desc)
            desc_label.setStyleSheet("font-size: 14px; color: #a0a0a0; margin-top: 4px;")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

        footer_layout = QHBoxLayout()
        if self.post.service:
            service_label = QLabel(self.post.service)
            service_label.setStyleSheet("""
                font-size: 12px;
                color: #ffffff;
                background: #4a90e2;
                padding: 4px 8px;
                border-radius: 6px;
            """)
            footer_layout.addWidget(service_label)

        footer_layout.addStretch()

        contact_icons = []
        if self.post.wechat: contact_icons.append("💬")
        if self.post.qq: contact_icons.append("🐧")
        if self.post.phone: contact_icons.append("📞")

        if contact_icons:
            contact_label = QLabel(" ".join(contact_icons))
            contact_label.setStyleSheet("font-size: 14px; color: #a0a0a0;")
            footer_layout.addWidget(contact_label)

        layout.addLayout(footer_layout)

    def mousePressEvent(self, event):
        self.animation.stop()
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(self.geometry().adjusted(2, 2, -2, -2))
        self.animation.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.animation.stop()
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(self.geometry().adjusted(-2, -2, 2, 2))
        self.animation.start()
        self.clicked.emit(self.post.id)
        super().mouseReleaseEvent(event)
