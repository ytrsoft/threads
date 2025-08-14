import sys
import os
from PyQt6.QtCore import Qt, QRect, QPoint
from PyQt6.QtGui import QPainter, QColor, QPixmap, QIcon, QLinearGradient
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout


class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(40)
        self.setAutoFillBackground(False)
        self.moving = False
        self.offset = QPoint()

        # 左侧图标
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap('default_frame_icon.png').scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio,
                                                                     Qt.TransformationMode.SmoothTransformation))
        # 标题
        self.title_label = QLabel('自定义暗黑窗体')
        self.title_label.setStyleSheet('color: white; font-size: 14px;')

        # 按钮
        self.btn_min = self.create_button('frame_min_normal.png', 'frame_min_rover.png', 'frame_min_pressed.png',
                                          self.parent.showMinimized)
        self.btn_max = self.create_button('frame_max_normal.png', 'frame_max_rover.png', 'frame_max_pressed.png',
                                          self.toggle_max_restore)
        self.btn_close = self.create_button('frame_close_normal.png', 'frame_close_rover.png', 'frame_close_pressed.png',
                                            self.parent.close)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(8)
        layout.addWidget(icon_label)
        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.btn_min)
        layout.addWidget(self.btn_max)
        layout.addWidget(self.btn_close)
        self.setLayout(layout)

    def create_button(self, normal, hover, pressed, callback):
        btn = QPushButton()
        btn.setFixedSize(30, 30)
        btn.setIcon(QIcon(normal))
        btn.setIconSize(btn.size())

        def enter_event(event):
            btn.setIcon(QIcon(hover))

        def leave_event(event):
            btn.setIcon(QIcon(normal))

        def press_event(event):
            btn.setIcon(QIcon(pressed))

        def release_event(event):
            btn.setIcon(QIcon(hover))
            callback()

        btn.enterEvent = enter_event
        btn.leaveEvent = leave_event
        btn.mousePressEvent = press_event
        btn.mouseReleaseEvent = release_event
        btn.setStyleSheet('background-color: transparent; border: none;')
        return btn

    def toggle_max_restore(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.moving = True
            self.offset = event.globalPosition().toPoint() - self.parent.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.moving and event.buttons() == Qt.MouseButton.LeftButton:
            self.parent.move(event.globalPosition().toPoint() - self.offset)

    def mouseReleaseEvent(self, event):
        self.moving = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor('#2c2c2c'))
        painter.setPen(QColor('#444'))
        painter.drawLine(0, self.height()-1, self.width(), self.height()-1)


class CustomWindow(QWidget):
    def __init__(self, title='自定义暗黑窗体', is_dialog=False):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumSize(500, 400)

        self.title_bar = TitleBar(self)
        self.title_bar.title_label.setText(title)

        layout = QVBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(0)
        layout.addWidget(self.title_bar)

        if not is_dialog:
            btn = QPushButton('弹出弹窗')
            btn.setFixedSize(150, 40)
            btn.setStyleSheet('''
                QPushButton {
                    background-color: #555;
                    color: white;
                    font-size: 14px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #777;
                }
            ''')
            btn.clicked.connect(self.show_dialog)
            content_layout = QVBoxLayout()
            content_layout.addStretch()
            content_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
            content_layout.addStretch()
            main_content = QWidget()
            main_content.setLayout(content_layout)
            main_content.setStyleSheet('background-color: #383838; border-radius: 0px;')
            layout.addWidget(main_content)
        else:
            label = QLabel('这是一个弹窗', alignment=Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet('color: white; font-size: 16px; background-color: #383838;')
            layout.addWidget(label)

        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 柔和阴影（透明渐变）
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 0, 0, 40))   # 顶部轻微阴影
        gradient.setColorAt(0.5, QColor(0, 0, 0, 15)) # 中间更淡
        gradient.setColorAt(1, QColor(0, 0, 0, 40))   # 底部轻微阴影
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(QRect(0, 0, self.width(), self.height()), 10, 10)

        # 主背景（无黑色边框）
        rect = QRect(0, 0, self.width(), self.height())
        painter.setBrush(QColor(40, 40, 40))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 10, 10)

    def show_dialog(self):
        dialog = CustomWindow(title='弹窗', is_dialog=True)
        dialog.setFixedSize(300, 200)
        dialog.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    win = CustomWindow()
    win.show()
    sys.exit(app.exec())
