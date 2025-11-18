from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QApplication
from app.help import HelpLogic
from app.database import SessionLocal, create_db
from app.models import *
from app.main_window import MainWindow
from os import path


class Login(QWidget):
    def __init__(self):
        super().__init__()

        create_db()
        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "ui", "login.ui"), self)
        self.setup_ui()

    def setup_ui(self):
        self.submit.clicked.connect(self.check_login)

    def check_login(self):
        username = self.username.text()

        session = SessionLocal()

        user = session.query(Users).filter_by(username=username).first()

        if user:
            password = session.query(Users).filter_by(username=username).first().password
            if  self.password.text() == password:
                main = MainWindow(username=username)   
                main.show()
                self.close()

            else:
                HelpLogic.error("كلمة المرور خاطئة")
        else:
            HelpLogic.error("لم يتم العثور على المستخدم")
    

if __name__ == '__main__':
    app = QApplication([])
    window = Login()
    window.show()
    app.exec()
