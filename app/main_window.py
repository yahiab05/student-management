from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QMainWindow, QApplication
from app.database import SessionLocal
from .devision import *
from .settings import SettingsLogic
from .models import Users
import gc
from .help import HelpLogic


class MainWindow(QMainWindow):
    def __init__(self, username, parent=None):
        super().__init__(parent)

        gc.disable()

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "main.ui"), self)
        
        self.username.setText(username)
        HelpLogic.set_username(username)
        self.acess()

        self.s = StudentsPart(self.stackedWidget)
        self.t = TeachersPart(self.stackedWidget)
        self.c = ClassPart(self.stackedWidget)
        self.u = UserPart(self.stackedWidget)
        self.m = MoneyPart(self.stackedWidget)
        self.p = PaymentPart(self.stackedWidget)
        self.a = AbsentsPart(self.stackedWidget)
        self.sett = SettingsLogic(self.stackedWidget)

        self.stackedWidget.addWidget(self.s)
        self.stackedWidget.addWidget(self.c)
        self.stackedWidget.addWidget(self.t)
        self.stackedWidget.addWidget(self.p)
        self.stackedWidget.addWidget(self.m)
        self.stackedWidget.addWidget(self.a)
        self.stackedWidget.addWidget(self.sett)
        self.stackedWidget.addWidget(self.u)

        self.setup_ui()


    def setup_ui(self):
        self.students.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.classes.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.teachers.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.payment.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.money.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.absents.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(6))
        self.settings.clicked.connect(self.go_settings)
        self.user.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(8))

    def go_settings(self):
        self.stackedWidget.setCurrentIndex(7)

    def closeEvent(self, event):
        gc.collect()
        event.accept()

    def acess(self):
        session = SessionLocal()

        query = session.query(Users).filter(Users.username == self.username.text()).first()

        self.students.setEnabled(query.role.students)
        self.classes.setEnabled(query.role.classes)
        self.teachers.setEnabled(query.role.teachers)
        self.payment.setEnabled(query.role.payment)
        self.money.setEnabled(query.role.money)
        self.absents.setEnabled(query.role.absent)
        self.settings.setEnabled(query.role.settings)
        self.user.setEnabled(query.role.user)

        session.close()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow('Yahia')
    window.show()
    app.exec()