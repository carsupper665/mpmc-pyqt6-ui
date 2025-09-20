#ui/my_server_page.py
import time
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QThread, QSettings
from logging import Logger
from src.constants import BASE_API, APP_VER, HEADER, SYSTEM_NAME
from ui.side_bar import SideBar

class MyServerPage(QWidget):
    def __init__(self, parent, logger: Logger):
        super().__init__(parent)
        self.LOGGER = logger

        self.p = self.parent()

        self.setObjectName("MyServerPage")

        self.page_layout = QHBoxLayout(self)
        self.page_layout.addWidget(SideBar(self.p))
        
        self.LOGGER.debug("🛠 My Server Page is ready!")

        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""      
                #MyServerPage {
                    background: #1E1E2F;
                    border-right: 1px solid #4B5870;
                }
                """)
        self.page_layout.setContentsMargins(0, 0, 0, 0)

        self.create_list()

    def create_list(self):

        list_layout = QVBoxLayout()
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(8)

        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(8)
        title = QLabel("My Server", self)
        title.setStyleSheet("""
            font-family: "Inter";
            font-size: 32px;
            color: #FFFFFF;
        """)
        
        title.setFixedHeight(50)
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        title_layout.addWidget(title)

        btn = QPushButton("Refresh", self)
        btn.setFixedHeight(32)

        title_layout.addWidget(btn)
        title_layout.addStretch()

        list_layout.addLayout(title_layout)
        list_layout.addStretch()
        self.page_layout.addLayout(list_layout)
        self.page_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.page_layout.addStretch()
