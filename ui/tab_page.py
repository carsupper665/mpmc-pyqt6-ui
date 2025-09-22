#ui/tab_page.py
import time
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QHBoxLayout, 
    QStackedLayout
)
from PyQt6.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QThread, QSettings
from logging import Logger
from src.constants import BASE_API, APP_VER, HEADER, SYSTEM_NAME
from ui import side_bar, my_server_page, add_server_page

class TabPage(QWidget):
    def __init__(self, parent, logger: Logger):
        super().__init__(parent, )

        self.LOGGER = logger

        self.parent = parent

        self.setObjectName(self.__class__.__name__)

        self.h_layout = QHBoxLayout(self)
        self.bar = side_bar.SideBar(self.parent)
        self.h_layout.addWidget(self.bar)

        self.stack_container = QWidget(self)
        self.stacker = QStackedLayout(self.stack_container)

        self.h_layout.addWidget(self.stack_container)

        self.my_server_page = my_server_page.MyServerPage(self, self.LOGGER)
        self.add_server_page = add_server_page.AddServerPage(self, self.LOGGER)

        pages = [QWidget(self),self.my_server_page, self.add_server_page]

        self.load_pages(pages)

        self.bar.nav_clicked.connect(self.set_page)

        self.stacker.setCurrentIndex(0)

    def load_pages(self, pages: list):
        for page in pages:
            self.stacker.addWidget(page)

    pyqtSlot(int)
    def set_page(self, index: int):
        self.stacker.setCurrentIndex(index)


        


