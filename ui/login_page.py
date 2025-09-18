# ui/login_page.py

import time
import requests
import keyring
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QThread, QSettings
from logging import Logger
from src.constants import BASE_API, APP_VER, HEADER, SYSTEM_NAME

class LoginPage(QWidget):
    start_login = pyqtSignal(str, str, requests.Session)
    show_next_page = pyqtSignal(int)
    def __init__(self, parent, logger: Logger):
        super().__init__(parent)
        self.LOGGER = logger
        self.parent = parent
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
        self.u_inp = QLineEdit(self.login_box)
        self.u_inp.setPlaceholderText("Username or Email")
        self.u_inp.setFixedHeight(70)
        self.u_inp.setStyleSheet("""
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
        box.addWidget(self.u_inp)

        # Password 段落
        self.p_inp = QLineEdit(self.login_box)
        self.p_inp.setPlaceholderText("Password")
        self.p_inp.setEchoMode(QLineEdit.EchoMode.Password)
        self.p_inp.setFixedHeight(70)
        self.p_inp.setStyleSheet("""
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
        box.addWidget(self.p_inp)

        # login error
        self.login_err = QLabel("", self.login_box)
        self.login_err.setStyleSheet("""
            font-family: "Inter";
            font-weight: 400;
            font-size: 14px;
            color: #FF6666;
        """)
        self.login_err.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.login_err.setWordWrap(True)
        box.addWidget(self.login_err)

        # Login 按鈕
        self.login_btn = QPushButton("LOGIN", self.login_box)
        self.login_btn.setFixedSize(147, 59)
        self.login_btn.setStyleSheet("""
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
        self.login_btn.clicked.connect(self.handle_login)
        box.addWidget(self.login_btn, 0, Qt.AlignmentFlag.AlignRight)

        root.addWidget(self.login_box)

        self.init_login()

        self.LOGGER.info("LoginPage initialized")

    def init_login(self):
        self.thread = QThread(self)
        self.worker = Login()
        self.worker.moveToThread(self.thread)

        self.worker.finished.connect(self.thread.quit)
        self.worker.res.connect(self.handel_res)
        self.start_login.connect(self.worker.do_login)

        self.show_next_page.connect(self.parent.show_page)
    
    def handle_login(self):
        username = self.u_inp.text()
        password = self.p_inp.text()
        if password == "" or username == "":
            self.login_err.setText(" 😠 😡 🤬: Username and password cannot be empty.")
            return
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Loading..")
        # 發送信號給外部去執行 Worker
        self.thread.start()
        self.start_login.emit(username, password, self.parent.session)

    @pyqtSlot(dict)
    def handel_res(self, data: dict):
        self.LOGGER.debug("Login....")

        self.login_btn.setEnabled(True)
        self.login_btn.setText("LOGIN")
        if data.get("next_page"):
            self.show_next_page.emit(data.get("next_page"))
        elif data.get("error") or data.get("Exception"):
            err_msg = data.get("error") if data.get("error") else str(data.get("Exception"))
            self.LOGGER.error("😢😭💔")
            self.LOGGER.error(f"Login error: {err_msg}")
            self.login_err.setText(f"😢😭💔 Error: {err_msg}")
            self.p_inp.setText("")
        if "data" in data:
            if data["data"].get("token"):
                setting = QSettings("Private Minecraft Server", SYSTEM_NAME)
                setting.setValue("username", self.u_inp.text())
                keyring.set_password(SYSTEM_NAME, self.u_inp.text(), data["data"].get("token", ""))
                keyring.set_password(SYSTEM_NAME, "device_id", data["headers"].get(HEADER, ""))
                self.show_next_page.emit(0)  # 返回到主頁面

class VerificationPage(QWidget):
    start_verfiy = pyqtSignal(str, requests.Session)
    show_next_page = pyqtSignal(int)
    def __init__(self, parent, logger: Logger):
        super().__init__(parent)
        self.LOGGER = logger
        self.parent = parent
        self.setObjectName("Verification Page")
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
        title = QLabel("Enter Your Code.", self.login_box)
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

        box.addSpacing(20)
        self.code = QLineEdit(self.login_box)
        self.code.setPlaceholderText("Your Verification Code: ")
        self.code.setFixedHeight(70)
        self.code.setStyleSheet("""
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
        box.addWidget(self.code)

        self.sumbit = QPushButton("SUMBIT", self.login_box)
        self.sumbit.setFixedSize(147, 59)
        self.sumbit.setStyleSheet("""
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
        # self.sumbit.clicked.connect(self.handle_sumbit)
        box.addWidget(self.sumbit, 0, Qt.AlignmentFlag.AlignRight)

        root.addWidget(self.login_box)

        self.init_verify()

    def init_verify(self,):
        self.sumbit.clicked.connect(self.handle_sumbit)
        self.verify_thread = QThread()
        self.v = Verify()
        self.v.moveToThread(self.verify_thread)

        self.v.finished.connect(self.verify_thread.quit)
        self.v.res.connect(self.handel_res)

        self.start_verfiy.connect(self.v.do_verify)
        self.show_next_page.connect(self.parent.show_page)

    def handle_sumbit(self):
        self.sumbit.setEnabled(False)
        self.sumbit.setText("...")
        code = self.code.text()
        self.verify_thread.start()
        self.start_verfiy.emit(code, self.parent.session)

    @pyqtSlot(dict)
    def handel_res(self, data: dict):
        self.LOGGER.debug(f"Verification returned: {data}")
        if "Exception" in data:
            self.sumbit.setEnabled(True)
            self.sumbit.setText("SUMBIT")
            self.code.setText("")
            self.code.setPlaceholderText("Error: " + str(data["Exception"]))
            return
        if "data" in data:
            if data["data"].get("token"):
                self.sumbit.setEnabled(False)
                self.sumbit.setText("Loading...")
                setting = QSettings("Private Minecraft Server", SYSTEM_NAME)
                setting.setValue("username", self.parent.login_page.u_inp.text())
                keyring.set_password(SYSTEM_NAME, self.parent.login_page.u_inp.text(), data["data"].get("token", ""))
                keyring.set_password(SYSTEM_NAME, "device_id", data["headers"].get(HEADER, ""))
                self.show_next_page.emit(0)  # 返回到主頁面
            else:
                self.sumbit.setEnabled(True)
                self.sumbit.setText("SUMBIT")
                self.code.setText("")
                self.code.setPlaceholderText("Error: ")
        self.sumbit.setEnabled(True)
        self.sumbit.setText("SUMBIT")

class Verify(QObject):
    res = pyqtSignal(dict)
    finished = pyqtSignal()

    @pyqtSlot(str, requests.Session)
    def do_verify(self, code: str, s: requests.Session):
        try:
            data = {}
            print(code)
            payload = {"code":code}
            headers = {"Content-Type": "application/json", }
            response = s.post(BASE_API + "/Authentication/app/verify", json=payload, headers=headers, timeout=10)
            data = response.json()
            headers = response.headers
            self.res.emit({"data": data, "headers": headers})
        except Exception as e:
            self.res.emit({"Exception":e})
        finally:
            self.finished.emit()

class Login(QObject):
    res = pyqtSignal(dict)
    finished = pyqtSignal()

    @pyqtSlot(str, str, requests.Session)
    def do_login(self, username: str, password: str, s: requests.Session):
        try:
            session = s
            if not session.headers.get(HEADER):
                print(session.headers.get(HEADER))
                session.headers.update({
                HEADER:"mpmc HUNS"})

            session.headers.update({
                "User-Agent": f"n-{APP_VER}-(mpmc client ua)"
            })

            email = ""

            if "@" in username:
                email = username
                username = ""
            
            print(username, password)

            payload = {"email":email,"username": username, "password": password}
            headers = {"Content-Type": "application/json", }
            response = session.post(BASE_API + "/Authentication/app/login", json=payload, headers=headers, timeout=10)

            if response.status_code == 200:
                # 取得 cookie dict
                cookie_dict = session.cookies.get_dict()
                data = response.json()  # 若有 JSON 回應
                print({"success": True, "cookies": cookie_dict, "data": data})
                self.res.emit({"data": data, "headers": response.headers})
            elif response.status_code == 202:
                session.headers.update({
                    HEADER: response.headers.get(HEADER, "")
                })
                self.res.emit({"next_page":2})
            else:
                self.res.emit({"error":f"status:{response.status_code} message:{response.text}"})
        except Exception as e:
            self.res.emit({"Exception":e})
        finally:
            self.finished.emit()
        




