#ui/my_server_page.py
import time
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QThread, QSettings, QTimer, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import QTransform, QIcon
from logging import Logger
from src.constants import BASE_API, APP_VER, HEADER, SYSTEM_NAME, IMAGES_URL


class MyServerPage(QWidget):
    def __init__(self, parent, logger: Logger):
        super().__init__(parent)
        self.LOGGER = logger

        self.p = self.parent()

        self.setObjectName("MyServerPage")

        self.page_layout = QHBoxLayout(self)
        
        self.LOGGER.debug("🛠 My Server Page is ready!")

        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""      
                #MyServerPage {
                    background: #1E1E2F;
                    border-right: 1px solid #4B5870;
                }
                QToolTip {
                    background-color: #2A3448;
                    color: #FFFFFF;
                    border: 1px solid #4B5870;
                    border-radius: 4px;
                    padding: 4px 6px;
                    margin: 0px;
                    font-family: "Inter";
                    font-size: 11px;
                    font-weight: normal;
                    white-space: nowrap;
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
            background: transparent;
            border: none;
        """)
        
        title.setFixedHeight(50)
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        title_layout.addWidget(title)

        # Create styled refresh button with icon
        btn = QPushButton(self)
        
        # Set tooltip for the button
        btn.setToolTip("重新整理伺服器列表")
        
        # Set refresh icon (we'll check if the icon exists, if not use text)
        try:
            refresh_icon = QIcon()
            refresh_icon.addFile(IMAGES_URL + '/icon_refresh.svg')
            btn.setIcon(refresh_icon)
            btn.setIconSize(QSize(20, 20))
        except:
            # Fallback to text if icon doesn't exist
            btn.setText("🔄")
        
        btn.setFixedSize(40, 40)
        btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 2px solid transparent;
                border-radius: 20px;
                padding: 8px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 20);
                border: 2px solid rgba(255, 255, 255, 30);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 40);
                border: 2px solid rgba(255, 255, 255, 50);
            }
            QPushButton:disabled {
                background: rgba(100, 100, 100, 30);
                border: 2px solid rgba(100, 100, 100, 50);
            }
        """)
        
        # Connect button click event
        btn.clicked.connect(self.on_refresh_clicked)
        self.refresh_btn = btn

        title_layout.addWidget(btn)
        title_layout.addStretch()

        list_layout.addLayout(title_layout)
        list_layout.addStretch()
        self.page_layout.addLayout(list_layout)
        self.page_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.page_layout.addStretch()

    def on_refresh_clicked(self):
        """Handle refresh button click with visual feedback"""
        self.LOGGER.info("🔄 Refreshing server list...")
        
        # Disable button temporarily to prevent spam clicking
        self.refresh_btn.setEnabled(False)
        
        # Create a timer to simulate refresh operation and re-enable button
        self.refresh_timer = QTimer()
        self.refresh_timer.setSingleShot(True)
        self.refresh_timer.timeout.connect(self.refresh_complete)
        self.refresh_timer.start(1500)  # Simulate 1.5 second refresh time
        
        # TODO: Add actual server refresh logic here
        # This is where you would make API calls to refresh server data
        
    def refresh_complete(self):
        """Called when refresh operation is complete"""
        # Reset button state
        self.refresh_btn.setEnabled(True)
        self.LOGGER.info("✅ Server list refreshed successfully!")
