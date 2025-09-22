#src/constants
#INFO
# APP_VER = "0.0.1-beta.0.0.1"
APP_VER     = "0.1.0"
SYSTEM_NAME = "MPMC-UI-Helper"
HEADER      = "C-MPMC-APP-Header"
# URL
# BASE_API = r"https://mc.yyanc9.com/api/"
BASE_API = r"http://localhost:8080"
IMAGES_URL = r"./src/images"
GLOBAL_FRONT = r"./src/fonts"

# QSS
QTOOLBUTTON_HOVER = """
QToolButton:hover {
        background-color:  rgba(255, 255, 255, 50); 
    }
"""
QPROGRESSBAR = """
            QProgressBar {
                background-color: #2A3448;
                border: 2px solid #CFD9FB;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #D6D0FA,
                    stop: 1 #657EAE
                );
                border-radius: 5px;
            }
        """
# Page index
LOGIN_PAGE = 1
# ---------------
MY_SERVER_PAGE = 1
ADD_SERVER_PAGE = 2