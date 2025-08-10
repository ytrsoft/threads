import sys
from sqlalchemy.orm import Session
from sqlite import Post, Category, Image, get_db, init_db
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QPushButton, QScrollArea, QFrame,
                            QSizePolicy, QListWidget, QListWidgetItem, QDialog,
                            QTabWidget, QTextEdit, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer, QUrl
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView

init_db()

class AnimatedButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._animation = QPropertyAnimation(self, b"geometry")
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

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
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
                color: #a0a0a0;
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
        """)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.load_categories()

    def load_categories(self):
        db: Session = next(get_db())
        categories = db.query(Category).all()

        all_item = QListWidgetItem(QIcon.fromTheme("view-list"), "全部")
        all_item.setData(Qt.ItemDataRole.UserRole, "")
        self.addItem(all_item)

        for category in categories:
            item = QListWidgetItem(QIcon.fromTheme("folder"), category.title)
            item.setData(Qt.ItemDataRole.UserRole, category.id)
            self.addItem(item)

        self.currentItemChanged.connect(self.on_category_changed)

    def on_category_changed(self, current, previous):
        if current:
            self.category_selected.emit(current.data(Qt.ItemDataRole.UserRole))

class PostCard(QFrame):
    clicked = pyqtSignal(str)

    def __init__(self, post: Post, parent=None):
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

class PostDetailDialog(QDialog):
    def __init__(self, post_id: str, parent=None):
        super().__init__(parent)
        self.post_id = post_id
        self.setup_ui()
        self.load_post_data()

    def setup_ui(self):
        self.setWindowIcon(QIcon.fromTheme("dialog-information"))
        screen = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen.width() * 0.8), int(screen.height() * 0.7))
        self.setStyleSheet("""
            QDialog {
                background: #252525;
                border: 1px solid #3a3a3a;
                border-radius: 10px;
            }
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical {
                border: none;
                background: #252525;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4a4a4a;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover { background: #5a5a5a; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        toolbar = QWidget()
        toolbar.setStyleSheet("background: #333333; border-top-left-radius: 10px; border-top-right-radius: 10px;")

        self.main_scroll = QScrollArea()
        self.main_scroll.setWidgetResizable(True)

        content = QWidget()
        content.setStyleSheet("background: #252525;")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(24, 24, 24, 24)
        self.content_layout.setSpacing(16)

        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 24px; font-weight: 600; color: #ffffff;")
        self.title_label.setWordWrap(True)
        self.content_layout.addWidget(self.title_label)

        self.meta_widget = QWidget()
        self.meta_layout = QHBoxLayout(self.meta_widget)
        self.meta_layout.setContentsMargins(0, 0, 0, 0)
        self.meta_layout.setSpacing(8)
        self.content_layout.addWidget(self.meta_widget)

        self.tags_widget = QWidget()
        self.tags_layout = QHBoxLayout(self.tags_widget)
        self.tags_layout.setContentsMargins(0, 0, 0, 0)
        self.tags_layout.setSpacing(8)
        self.content_layout.addWidget(self.tags_widget)

        self.image_scroll = QScrollArea()
        self.image_scroll.setWidgetResizable(True)
        self.image_scroll.setStyleSheet("background: transparent;")
        self.image_scroll.setMinimumHeight(180)
        self.image_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.image_container = QWidget()
        self.image_layout = QHBoxLayout(self.image_container)
        self.image_layout.setContentsMargins(0, 0, 0, 0)
        self.image_layout.setSpacing(8)
        self.image_scroll.setWidget(self.image_container)
        self.content_layout.addWidget(self.image_scroll)

        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane { border: none; background: #252525; }
            QTabBar::tab {
                padding: 8px 16px;
                color: #a0a0a0;
                font-size: 14px;
                background: #333333;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 4px;
            }
            QTabBar::tab:selected { color: #ffffff; background: #4a90e2; }
            QTabBar::tab:hover { background: #3a3a3a; }
        """)

        self.detail_tab = QWidget()
        self.detail_layout = QVBoxLayout(self.detail_tab)
        self.detail_layout.setContentsMargins(0, 16, 0, 0)
        self.desc_label = QLabel()
        self.desc_label.setStyleSheet("font-size: 14px; color: #b0b0b0;")
        self.desc_label.setWordWrap(True)
        self.desc_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.detail_layout.addWidget(self.desc_label)
        self.detail_layout.addStretch()
        self.tab_widget.addTab(self.detail_tab, "详情")

        self.contact_tab = QWidget()
        self.contact_layout = QVBoxLayout(self.contact_tab)
        self.contact_layout.setContentsMargins(0, 16, 0, 0)
        self.contact_layout.setSpacing(12)
        self.contact_info = QTextEdit()
        self.contact_info.setStyleSheet("""
            QTextEdit {
                font-size: 14px;
                color: #b0b0b0;
                background: #333333;
                border: 1px solid #3a3a3a;
                border-radius: 6px;
                padding: 12px;
            }
        """)
        self.contact_info.setReadOnly(True)
        self.contact_layout.addWidget(self.contact_info)

        self.copy_button = AnimatedButton("复制联系方式")
        self.copy_button.setStyleSheet("""
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
        self.copy_button.clicked.connect(self.copy_contact_info)
        self.contact_layout.addWidget(self.copy_button, 0, Qt.AlignmentFlag.AlignRight)
        self.contact_layout.addStretch()
        self.tab_widget.addTab(self.contact_tab, "联系方式")

        self.content_layout.addWidget(self.tab_widget)
        self.content_layout.addStretch()
        self.main_scroll.setWidget(content)
        layout.addWidget(self.main_scroll)

        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(30)
        effect.setColor(QColor(0, 0, 0, 150))
        effect.setOffset(0, 5)
        self.setGraphicsEffect(effect)

    def load_post_data(self):
        db: Session = next(get_db())
        post = db.query(Post).filter(Post.id == self.post_id).first()
        if not post: return

        self.title_label.setText(post.title)
        self.clear_layout(self.meta_layout)

        for text, icon in [
            (post.region, "📍"),
            (post.age, "👧"),
            (post.score, "⭐"),
            (post.price, "💰")
        ]:
            if text:
                label = QLabel(f"{icon} {text}")
                label.setStyleSheet("""
                    font-size: 14px;
                    color: #b0b0b0;
                    padding: 6px 12px;
                    background: #333333;
                    border-radius: 6px;
                """)
                self.meta_layout.addWidget(label)

        self.meta_layout.addStretch()
        self.clear_layout(self.tags_layout)

        if post.service:
            service_label = QLabel(post.service)
            service_label.setStyleSheet("""
                font-size: 14px;
                color: #ffffff;
                background: #4a90e2;
                padding: 6px 12px;
                border-radius: 6px;
            """)
            self.tags_layout.addWidget(service_label)

        self.tags_layout.addStretch()
        self.desc_label.setText(post.desc if post.desc else "暂无详细描述")

        contact_text = ""
        if post.wechat: contact_text += f"微信: {post.wechat}\n"
        if post.qq: contact_text += f"QQ: {post.qq}\n"
        if post.phone: contact_text += f"电话: {post.phone}\n"
        self.contact_info.setPlainText(contact_text if contact_text else "暂无联系方式")

        self.load_images(post.id)


    def load_images(self, post_id):
        db: Session = next(get_db())
        images = db.query(Image).filter(Image.pid == post_id).all()
        self.clear_layout(self.image_layout)

        if not images:
            no_image_label = QLabel("暂无图片")
            no_image_label.setStyleSheet("font-size: 14px; color: #a0a0a0; padding: 16px;")
            self.image_layout.addWidget(no_image_label)
            return

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(8)

        image_height = 180
        image_gap = 8
        images_per_row = 3

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                ::-webkit-scrollbar {{
                    display: none;
                    width: 0;
                    height: 0;
                    background: transparent;
                }}
                body {{
                    background-color: #2a2a2a;
                    margin: 0;
                    padding: 8px;
                    font-family: Arial, sans-serif;
                }}
                .image-container {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: {image_gap}px;
                }}
                .image-item {{
                    width: calc((100% - {image_gap * (images_per_row - 1)}px) / {images_per_row});
                    height: {image_height}px;
                    background-color: #333333;
                    border-radius: 6px;
                    border: 1px solid #3a3a3a;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    overflow: hidden;
                }}
                .image-item img {{
                    max-width: 100%;
                    max-height: 100%;
                    object-fit: contain;
                }}
                .error-message {{
                    color: #ff6464;
                    text-align: center;
                    padding: 16px;
                }}
            </style>
        </head>
        <body>
            <div class="image-container">
        """

        for image in images:
            if hasattr(image, 'src') and image.src:
                html_content += f"""
                <div class="image-item">
                    <img src="{image.src}" onerror="this.parentElement.innerHTML='<div class=\\'error-message\\'>图片加载失败</div>'" />
                </div>
                """
            else:
                html_content += """
                <div class="image-item">
                    <div class="error-message">无效图片URL</div>
                </div>
                """

        html_content += """
            </div>
        </body>
        </html>
        """

        web_view = QWebEngineView()
        web_view.setHtml(html_content, QUrl("about:blank"))
        web_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        scroll_layout.addWidget(web_view)
        scroll_content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.image_scroll.setWidget(scroll_content)
        self.image_scroll.setWidgetResizable(True)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    def copy_contact_info(self):
        QApplication.clipboard().setText(self.contact_info.toPlainText())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_page = 1
        self.current_category = ""
        self.search_keyword = ""
        self.has_more = True
        self.loading = False

        self.setup_ui()
        self.load_posts()

        screen = QApplication.primaryScreen().availableGeometry()
        self.resize(int(screen.width() * 0.8), int(screen.height() * 0.7))

    def setup_ui(self):
        self.setWindowIcon(QIcon.fromTheme("system-search"))
        self.setStyleSheet("""
            QMainWindow { background: #1a1a1a; }
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical {
                border: none;
                background: #252525;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4a4a4a;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover { background: #5a5a5a; }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = QWidget()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("background: #252525; border-right: 1px solid #3a3a3a;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("数据平台")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: 600;
            color: #ffffff;
            padding: 24px;
            border-bottom: 1px solid #3a3a3a;
        """)
        sidebar_layout.addWidget(title)

        self.category_menu = CategoryMenu()
        sidebar_layout.addWidget(self.category_menu)

        main_layout.addWidget(sidebar)

        content = QWidget()
        content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(16)

        search_container = QWidget()
        search_container.setFixedHeight(60)
        search_container.setStyleSheet("background: #2a2a2a; border-radius: 8px;")
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(16, 8, 16, 8)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索内容...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: none;
                font-size: 14px;
                color: #ffffff;
                background: transparent;
            }
        """)
        self.search_input.returnPressed.connect(self.on_search)
        search_layout.addWidget(self.search_input)

        search_button = QPushButton("搜索")
        search_button.setStyleSheet("""
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
        search_button.clicked.connect(self.on_search)
        search_layout.addWidget(search_button)
        content_layout.addWidget(search_container)

        self.result_count = QLabel()
        self.result_count.setStyleSheet("font-size: 14px; color: #a0a0a0;")
        content_layout.addWidget(self.result_count)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.check_scroll)

        self.scroll_content = QWidget()
        self.scroll_content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(16)

        self.grid_layout = QVBoxLayout()
        self.grid_layout.setSpacing(16)
        self.scroll_layout.addLayout(self.grid_layout)

        self.load_more_label = QLabel("正在加载更多...")
        self.load_more_label.setStyleSheet("""
            font-size: 14px;
            color: #a0a0a0;
            padding: 16px;
            text-align: center;
        """)
        self.load_more_label.hide()
        self.scroll_layout.addWidget(self.load_more_label)
        self.scroll_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_content)
        content_layout.addWidget(self.scroll_area)
        main_layout.addWidget(content, stretch=1)

        self.category_menu.category_selected.connect(self.on_category_selected)

    def check_scroll(self):
        scroll_bar = self.scroll_area.verticalScrollBar()
        if scroll_bar.value() >= scroll_bar.maximum() - 100 and not self.loading and self.has_more:
            self.loading = True
            self.load_more_label.show()
            QTimer.singleShot(300, self.load_more_posts)

    def load_posts(self, reset=True):
        if reset:
            self.current_page = 1
            self.has_more = True
            while self.grid_layout.count():
                item = self.grid_layout.takeAt(0)
                if item.widget(): item.widget().deleteLater()

        db: Session = next(get_db())
        query = db.query(Post)

        if self.current_category:
            query = query.filter(Post.mid == self.current_category)

        if self.search_keyword:
            search = f"%{self.search_keyword}%"
            query = query.filter(
                Post.title.like(search) |
                Post.desc.like(search) |
                Post.region.like(search) |
                Post.age.like(search) |
                Post.score.like(search) |
                Post.price.like(search) |
                Post.service.like(search)
            )

        total = query.count()
        self.result_count.setText(f"共找到 {total} 条结果")

        per_page = 15
        posts = query.order_by(Post.id.desc()).offset(
            (self.current_page - 1) * per_page).limit(per_page).all()

        if not posts:
            self.has_more = False
            if reset:
                no_data = QLabel("没有找到数据")
                no_data.setStyleSheet("""
                    font-size: 14px;
                    color: #a0a0a0;
                    padding: 24px;
                    text-align: center;
                """)
                self.grid_layout.addWidget(no_data)
            return

        for post in posts:
            card = PostCard(post)
            card.clicked.connect(self.show_post_detail)
            self.grid_layout.addWidget(card)

    def load_more_posts(self):
        if not self.has_more:
            self.load_more_label.hide()
            return

        self.current_page += 1
        db: Session = next(get_db())
        query = db.query(Post)

        if self.current_category:
            query = query.filter(Post.mid == self.current_category)

        if self.search_keyword:
            search = f"%{self.search_keyword}%"
            query = query.filter(
                Post.title.like(search) |
                Post.desc.like(search) |
                Post.region.like(search) |
                Post.age.like(search) |
                Post.score.like(search) |
                Post.price.like(search) |
                Post.service.like(search)
            )

        per_page = 15
        posts = query.order_by(Post.id.desc()).offset(
            (self.current_page - 1) * per_page).limit(per_page).all()

        for post in posts:
            card = PostCard(post)
            card.clicked.connect(self.show_post_detail)
            self.grid_layout.addWidget(card)

        total = query.count()
        self.has_more = (self.current_page * per_page) < total
        self.loading = False
        self.load_more_label.hide()

    def on_category_selected(self, category_id):
        self.current_category = category_id
        self.load_posts()

    def on_search(self):
        self.search_keyword = self.search_input.text().strip()
        self.load_posts()

    def show_post_detail(self, post_id):
        detail_dialog = PostDetailDialog(post_id, self)
        detail_dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont()
    font.setFamily("Segoe UI" if sys.platform == "win32" else "SF Pro Display")
    app.setFont(font)

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(26, 26, 26))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.Text, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.Highlight, QColor(74, 144, 226))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
