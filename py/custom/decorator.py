from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QApplication


def create_logo(icon_path='default_frame_icon.png'):
    _btn = QPushButton()
    _btn.setFixedSize(20, 20)
    _btn.setIcon(QIcon(icon_path))
    _btn.setIconSize(_btn.size())
    _btn.setStyleSheet('background-color: transparent; border: none;')
    return _btn


class TitleButton(QPushButton):
    def __init__(self, state, clicked_callback=None):
        super().__init__()
        self.state = state
        self.clicked_callback = clicked_callback
        self.setFixedSize(16, 16)
        self.update_icon('normal')
        self.setStyleSheet('background-color: transparent; border: none;')

    def update_icon(self, suffix):
        icon_state = 'maxwin' if self.window().isMaximized() and self.state == 'max' else self.state
        self.setIcon(QIcon(f'frame_{icon_state}_{suffix}.png'))
        self.setIconSize(self.size())

    def enterEvent(self, event):
        self.update_icon('rover')
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.update_icon('normal')
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.update_icon('pressed')
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.update_icon('normal')
            if self.clicked_callback:
                self.clicked_callback()
        super().mouseReleaseEvent(event)


class QtWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.top_widget = QWidget()
        self.main_widget = QWidget()
        self.title = QLabel('')
        self.main_layout = None
        self.moving = False
        self.offset = QPoint()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        screen = QApplication.primaryScreen().availableGeometry()
        width = int(screen.width() * 0.7)
        height = int(screen.height() * 0.7)
        self.resize(width, height)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.top_widget.setFixedHeight(48)
        self.top_widget.setStyleSheet(
            'background-color: #2B2D30; border-top-left-radius: 8px; border-top-right-radius: 8px;'
        )

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(12, 0, 12, 0)

        logo = create_logo()
        self.title.setStyleSheet('color: #B7B9BF; font-weight: bold')
        min_btn = TitleButton('min', self.showMinimized)
        max_btn = TitleButton('max', self.toggle_max_restore)
        close_btn = TitleButton('close', self.close)

        top_layout.addWidget(logo)
        top_layout.addSpacing(0)
        top_layout.addWidget(self.title)
        top_layout.addStretch()
        top_layout.addWidget(min_btn)
        top_layout.addSpacing(12)
        top_layout.addWidget(max_btn)
        top_layout.addSpacing(12)
        top_layout.addWidget(close_btn)
        self.top_widget.setLayout(top_layout)

        self.main_widget.setStyleSheet(
            'background-color: #1E1F22; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px;'
        )

        layout.addWidget(self.top_widget)
        layout.addWidget(self.main_widget, 1)

        self.main_layout = QHBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(12, 0, 12, 0)

    def set_title(self, text):
        self.title.setText(text)


    def toggle_max_restore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.moving = True
            self.offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.moving and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.offset)

    def mouseReleaseEvent(self, event):
        self.moving = False
