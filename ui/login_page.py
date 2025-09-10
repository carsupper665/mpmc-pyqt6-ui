# ui/login_page.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt
from logging import Logger

class LoginPage(QWidget):
    def __init__(self, parent, logger: Logger):
        super().__init__(parent)
        self.LOGGER = logger
        self.setObjectName("Login-UI-kit")
        self.setStyleSheet("background-color: none;")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(20)
        root.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.login_box = QWidget(self)
        self.login_box.setFixedSize(501, 600)
        self.login_box.setStyleSheet("""
            background-color: #4B5870;
            border-radius: 57px;
        """)
        box = QVBoxLayout(self.login_box)
        box.setContentsMargins(40, 40, 40, 40)
        box.setSpacing(20)
        box.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 大字
        title = QLabel("HI, my friend!", self.login_box)
        title.setStyleSheet("""
            font-family: "Inter";
            font-weight: 700;
            font-size: 48px;
            color: #FFFFFF;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        box.addWidget(title)

        # 小字
        subtitle = QLabel("Who goes there? No password, no cookies.", self.login_box)
        subtitle.setStyleSheet("""
            font-family: "Inter";
            font-weight: 500;
            font-size: 20px;
            color: #FFFFFF;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        box.addWidget(subtitle)

        # Username 段落
        box.addSpacing(20)
        u_inp = QLineEdit(self.login_box)
        u_inp.setPlaceholderText("Username or Email")
        u_inp.setFixedHeight(70)
        u_inp.setStyleSheet("""
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #D6D0FA, stop:1 #CFD9FB);
                border: none;
                border-radius: 20px;
                font-family: "Inter";
                font-weight: 400;
                font-size: 16px;
                color: #2A3448;
                padding-left: 12px;
            }
        """)
        box.addWidget(u_inp)

        # Password 段落
        p_inp = QLineEdit(self.login_box)
        p_inp.setPlaceholderText("Password")
        p_inp.setEchoMode(QLineEdit.EchoMode.Password)
        p_inp.setFixedHeight(70)
        p_inp.setStyleSheet("""
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #D6D0FA, stop:1 #CFD9FB);
                border: none;
                border-radius: 20px;
                font-family: "Inter";
                font-weight: 400;
                font-size: 16px;
                color: #2A3448;
                padding-left: 12px;
            }
        """)
        box.addWidget(p_inp)

        # Login 按鈕
        login_btn = QPushButton("LOGIN", self.login_box)
        login_btn.setFixedSize(147, 59)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #00141A;
                font-family: "Roboto";
                font-weight: 500;
                font-size: 28px;
                color: #E8EBF2;
                border: none;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #002A33;
                border: none;
                border-radius: 25px;
            }
        """)
        box.addWidget(login_btn, 0, Qt.AlignmentFlag.AlignRight)

        root.addWidget(self.login_box)
        self.LOGGER.info("LoginPage initialized")
