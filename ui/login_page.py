#ui/login_page.py
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QToolButton,
    QWidget,
    QStackedLayout,
    QVBoxLayout,
    QProgressBar,
)
from PyQt6.QtGui import QPalette, QIcon, QFont, QFontDatabase
from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSlot

from src import constants as c
from logging import Logger

class LoginPage(QWidget):
    def __init__(self, parent, logger : Logger):
        super().__init__(parent)
        self.LOGGER = logger

        self.setObjectName("Loging UI-Kit")

        self.setStyleSheet("background-color: none;")

        # 外層垂直排版 (置中 login box)
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addStretch()  # 上方留白

        # ===== 登入框 (等同你的 CSS login box) =====
        self.login_box = QWidget(self)
        self.login_box.setObjectName("loginBox")
        self.login_box.setFixedSize(501, 544)
        self.login_box.setStyleSheet("""
            QWidget#loginBox {
                background-color: #4B5870;
                border-radius: 57px;
            }
        """)

        # 在登入框裡面放排版
        box_layout = QVBoxLayout(self.login_box)
        box_layout.setContentsMargins(40, 40, 40, 40)
        box_layout.setSpacing(20)

        # 範例元件：標題 + 輸入欄位提示
        title = QLabel("登入", self.login_box)
        title.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        box_layout.addWidget(title)

        root_layout.addWidget(self.login_box, 0, Qt.AlignmentFlag.AlignHCenter)
        root_layout.addStretch()  # 下方留白

        self.LOGGER.info("LoginPage initialized")