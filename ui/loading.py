#ui/loading.py
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

class LoadingPage(QWidget):
    def __init__(self, parent, logger: Logger):
        self.LOGGER = logger
        super().__init__(parent)
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(12)
        v.addStretch()
        self.label = QLabel("Loading...", self)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label.setStyleSheet("""
                background-color: none;
                font-family: "Inter";
                font-style: normal;
                font-weight: 500;
                font-size: 20px;
                color: #FFFFFF;
                                 
            """)
        self.bar = QProgressBar(self)
        self.bar.setRange(0, 100)  # 不定長度可改成 (0,0)
        # self.bar.setValue(20)
        self.bar.setTextVisible(False) 
        self.bar.setFixedSize(985, 42)

        self.bar.setStyleSheet(c.QPROGRESSBAR)

        v.addWidget(self.label); v.addWidget(self.bar, alignment=Qt.AlignmentFlag.AlignHCenter)
    
        v.addStretch()
        self.LOGGER.info("Loading start..")

    @pyqtSlot(dict)
    def update_progress(self, data: dict):
        id = data.get("signalId")
        value = data.get("value")
        status_text = data.get("status")

        if (value is None) and (status_text is None) or (id is None):
            if id is None:
                self.LOGGER.debug("WARN::ID CANT BE NONE")
            self.LOGGER.error(f"Error: value and status_text can't be none")
            return
        try:
            if value is not None and type(value) == int:
                self.bar.setValue(value)
            if status_text is not None:
                self.label.setText(status_text)
        except Exception as e:
            self.LOGGER.critical(f"UI update progress error: {"\n"} {e.with_traceback()}")
            return
        
