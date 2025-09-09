import sys
import time
from PyQt6.QtCore import QObject, QThread, pyqtSignal, pyqtSlot, Qt, QEvent, QTimer, QSize
from PyQt6.QtGui import QPalette, QIcon, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QStackedLayout
)

from src.constants import *
from src.logger import get_logger

from ui.custom_title import CustomTitleBar
from ui.loading import LoadingPage

class Worker(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    @pyqtSlot()
    def run(self):
        for i in range(101):
            time.sleep(0.05)
            self.progress.emit(i)
        self.finished.emit()

# 建立主視窗類別
class MainWindow(QMainWindow):
    def __init__(self, log_level: int = 10, save_log: bool = True):
        self.LOGGER = get_logger(name=SYSTEM_NAME, level=log_level) # 還須修改
        self.LOGGER.debug("HI")
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.resize(1280, 720)
        self.create_main_window()
        self.set_content_container()

    def create_main_window(self):
        self.main_container = QWidget()
        self.main_container.setStyleSheet("background-color: #00081C;")
        self.main_layout = QVBoxLayout(self.main_container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # 使用自訂 TitleBar
        self.titlebar = CustomTitleBar(self)

        self.main_layout.addWidget(self.titlebar)
        self.main_layout.addStretch()

        self.setCentralWidget(self.main_container)           # 設定視窗大小

    def set_content_container(self):
        self.content_container = QWidget()
        self.content_layout_container = QStackedLayout(self.content_container)
        self.content_layout_container.setStackingMode(QStackedLayout.StackingMode.StackOne)

        loading_page = LoadingPage(self)
        loading_page.setStyleSheet("background-color: #1E293B;")

        self.content_layout_container.addWidget(loading_page)

        # 設定預設顯示的頁面
        self.content_layout_container.setCurrentIndex(0)

        # 把內容容器放到 main_layout，伸展係數=1 填滿剩餘空間
        self.main_layout.addWidget(self.content_container, 1)

        self.setCentralWidget(self.main_container)

    def add_page(self, pages: list):
        for pags in pages:
            self.content_layout_container.addWidget(pags)


if __name__ == "__main__":
    app = QApplication(sys.argv)   # 建立應用程式物件
    app.setFont(QFont(GLOBAL_FRONT))
    window = MainWindow()          # 建立主視窗
    window.show()                  # 顯示視窗
    sys.exit(app.exec())           # 進入事件迴圈
