#main_ui.py
import sys
import time
import keyring
import requests
from PyQt6.QtCore import QObject, QThread, pyqtSignal, pyqtSlot, Qt, QEvent, QTimer, QSize, QSettings
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
from src.logger import loggerFactory

from ui.custom_title import CustomTitleBar
from ui.loading import LoadingPage
from ui import login_page

from logging import Logger


class StartUp(QObject):
    # 進度條分配 載入頁面(25)->載入登入資訊(25)->登入(25)->載入使用者資料(25)->100
    # 登入失敗 -> 直接100 -> loginPage
    progress = pyqtSignal(dict)
    finished = pyqtSignal()
    show_next_page = pyqtSignal(int)

    @pyqtSlot(int)
    def run(self, start: int):
        id = self.__class__.__name__
        value = start
        next_page = 1
        username, token = self.load_user_info()
        value += 10
        self.emit_helper(id, value, "Loading User Info...")
        time.sleep(1)  # 模擬載入使用者資訊時間
        if username and token:
            self.emit_helper(id, value + 10, "Logging in...")
            time.sleep(1)  # 模擬登入時間
            # 假設登入成功
            self.emit_helper(id, value + 20, "Loading User Data...")
            time.sleep(1)  # 模擬載入使用者資料時間
            self.emit_helper(id, 100, "Welcome back!")
            time.sleep(0.5)
            next_page = 2  # 顯示主頁面
        else:
            self.emit_helper(id, None, "Welcome!, No user data found.")
            
            for i in range(value, 101):
                self.emit_helper(id, i, None)
                time.sleep(0.02)
        
        self.show_next_page.emit(next_page)  # 顯示登入頁面
        self.finished.emit()

    def emit_helper(self, id: str, value: int, status: str):
        self.progress.emit({"signalId": id, "value": value, "status": status})

    def load_user_info(self):
        self.setting = QSettings("Private Minecraft Server", SYSTEM_NAME)
        username = self.setting.value("username", "", type=str)
        Token = keyring.get_password(SYSTEM_NAME, username) if username else ""
        return username, Token

# 建立主視窗類別
class MainWindow(QMainWindow):
    progress = pyqtSignal(dict)
    start_startup = pyqtSignal(int)
    def __init__(self,  logger: Logger):
        self.LOGGER = logger
        self.LOGGER.info("✨ HI, from UI Init System ✨")
        self.session = requests.session()
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.resize(1280, 720)
        self.create_main_window()
        self.set_content_container()
        self.load_pages()

        self.start_worker()

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
        self.LOGGER.debug("🎉 Main Window is ready!")

    def set_content_container(self):
        self.content_container = QWidget()
        self.content_layout_container = QStackedLayout(self.content_container)
        self.content_layout_container.setStackingMode(QStackedLayout.StackingMode.StackOne)

        self.loading_page = LoadingPage(self, self.LOGGER)
        self.progress.connect(self.loading_page.update_progress)
        self.loading_page.setStyleSheet("background-color: #1E293B;")

        self.content_layout_container.addWidget(self.loading_page)

        # 設定預設顯示的頁面
        self.content_layout_container.setCurrentIndex(0)

        # 把內容容器放到 main_layout，伸展係數=1 填滿剩餘空間
        self.main_layout.addWidget(self.content_container, 1)

        self.setCentralWidget(self.main_container)
        self.LOGGER.debug("✨ Container is ready!")

    def load_pages(self):
        self.login_page = login_page.LoginPage(self, self.LOGGER)
        self.verify_page = login_page.VerificationPage(self, self.LOGGER)
        pages = [self.login_page, self.verify_page]
        self.add_page(pages)


    def start_worker(self):
        self.thread = QThread(self)
        self.worker = StartUp()
        self.worker.moveToThread(self.thread)

        self.worker.progress.connect(self.loading_page.update_progress)
        self.worker.finished.connect(self.thread.quit)
        self.worker.show_next_page.connect(self.show_page)

        # --- 啟動 ---
        self.thread.start()

        self.start_startup.connect(self.worker.run)
        self.start_startup.emit(25)

    def add_page(self, pages: list):
        step = 25 // len(pages)
        i = 0
        for page in pages:
            self.loading_page.label.setText(f"Loading: {page.objectName()}")
            self.content_layout_container.addWidget(page)
            i += step
            self.loading_page.bar.setValue(i)

    @pyqtSlot(int)
    def show_page(self, index: int):
        self.content_layout_container.setCurrentIndex(index)

if __name__ == "__main__":
    LOGSYS = loggerFactory(logger_name="M.P.M.C-Helper", log_level="DEBUG", write_log=False, file_name="SYS-LOG")
    LOGGER = LOGSYS.getLogger()
    LOGGER.debug("Here is log system. :D")
    app = QApplication(sys.argv)   # 建立應用程式物件
    app.setFont(QFont(GLOBAL_FRONT))
    window = MainWindow(logger=LOGGER)          # 建立主視窗
    window.show()                  # 顯示視窗
    sys.exit(app.exec())           # 進入事件迴圈
