from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QToolButton,
    QWidget,
    QStackedLayout
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QPalette, QIcon

from src import constants as c

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.is_parent_max = False
        self.parent = parent
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.ColorRole.Highlight)
        self.setFixedHeight(45)
        self.initial_pos = None
        self._mouse_pos = None

        title_bar_layout = QStackedLayout(self)
        title_bar_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        title_bar_layout.setContentsMargins(1, 1, 1, 1)
        title_bar_layout.setSpacing(2)

        btn_row = QWidget(self)
        btn_row.setStyleSheet("background-color: none;")
        btn_layout = QHBoxLayout(btn_row)
        btn_layout.setContentsMargins(1, 1, 8, 1)
        btn_layout.setSpacing(6)
        btn_layout.addStretch()

        self.title = QLabel(f"M。P。M。C", self)
        self.title.setStyleSheet(
            """font-weight: bold;
               border: 2px solid white;
               border-radius: 12px;
               margin: 2px;
               background-color: black;
            """
        )
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if title := parent.windowTitle():
            self.title.setText(title)
        title_bar_layout.addWidget(self.title)

        self.min_button = QToolButton(self)
        min_icon = QIcon()
        min_icon.addFile(c.IMAGES_URL + '/min_btn.png')
        self.min_button.setIcon(min_icon)
        self.min_button.clicked.connect(self.minimize_window)

        self.max_button = QToolButton(self)
        max_icon = QIcon()
        max_icon.addFile(c.IMAGES_URL + "/max_btn.png")
        self.max_button.setIcon(max_icon)
        self.max_button.clicked.connect(self.change_window)

        self.close_button = QToolButton(self)
        close_icon = QIcon()
        close_icon.addFile(c.IMAGES_URL + "/close_btn.png")
        self.close_button.setIcon(close_icon)
        self.close_button.clicked.connect(self.parent.close)

        self.normal_button = QToolButton(self)
        self.normal_button.setIcon(max_icon)
        self.normal_button.clicked.connect(self.change_window)
        self.normal_button.setVisible(False)
        buttons = [
            self.min_button,
            self.normal_button,
            self.max_button,
            self.close_button,
        ]
        for button in buttons:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setFixedSize(QSize(42, 42))
            button.setIconSize(QSize(24, 24))
            button.setStyleSheet("""QToolButton { 
                                 border: none;
                                 border-radius: 20px;}""" + "\n" + c.QTOOLBUTTON_HOVER
            )
            btn_layout.addWidget(button)

        self.close_button.setStyleSheet(
                """QToolButton { border: none;
                                 border-radius: 20px;
                                }
                    QToolButton:hover {
                    background-color:  rgba(229, 34, 34, 255); 
                }""" )
        
        title_bar_layout.addWidget(btn_row)
        
        title_bar_layout.setCurrentIndex(1 - title_bar_layout.currentIndex())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._mouse_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self._mouse_pos is not None:
            delta = event.globalPosition().toPoint() - self._mouse_pos
            self.parent.move(self.parent.x() + delta.x(),
                             self.parent.y() + delta.y())
            self._mouse_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self._mouse_pos = None

    def change_window(self,):
        if self.is_parent_max:
            self.is_parent_max = False
            self.parent.showNormal()
            self.max_button.setVisible(True)
            self.normal_button.setVisible(False)
        else:
            self.parent.showMaximized()
            self.is_parent_max = True
            self.max_button.setVisible(False)
            self.normal_button.setVisible(True)

    def minimize_window(self):
        QTimer.singleShot(20, lambda: self.parent.setWindowState(Qt.WindowState.WindowMinimized))