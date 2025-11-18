from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QApplication
from os import path
from .teacher import TeacherLogic, TeachersHistoryLogic
from .classes import ClassesLogic, ClasseleveLogic
from .students import StudentsHistoryLogic, StudentsLogic, ClassesPerStudentLogic
from .payment import AddPayment, ViewPayment, ViewNotPayedLogic
from .user import UserLogic, RoleLogic
from .money import BankLogic, CaisseLogic, EnteryLogic, OutMoneyLogic, BalanceLogic
from .teacher_absent import AddAbscentTLogic, ViewAbsentTeacherLogic
from .student_absent import AddAbsentStudentLogic, ViewAbsentStudentLogic


class StudentsPart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "studentpart.ui"), self)

        self.s = StudentsLogic(self)
        self.sh = StudentsHistoryLogic(self)
        self.cps = ClassesPerStudentLogic(self)

        self.stackedWidget.addWidget(self.s)
        self.stackedWidget.addWidget(self.sh)
        self.stackedWidget.addWidget(self.cps)

        self.stackedWidget.setCurrentIndex(0)
        self.buttons(self.students)

        self.setup()

    def setup(self):
        self.students.clicked.connect(self.go_to_students)
        self.students_history.clicked.connect(self.go_to_history)
        self.classes_per_student.clicked.connect(self.go_to_classes_per_student)

    def go_to_students(self):
        self.stackedWidget.setCurrentIndex(0)
        self.buttons(self.students)

    def go_to_history(self):
        self.stackedWidget.setCurrentIndex(1)
        self.sh.setup_table()
        self.buttons(self.students_history)

    def go_to_classes_per_student(self):
        self.stackedWidget.setCurrentIndex(2)
        self.cps.setup_table()
        self.buttons(self.classes_per_student)

    def buttons(self, button):
        self.students.setStyleSheet("color: white")
        self.students_history.setStyleSheet("color: white")
        self.classes_per_student.setStyleSheet("color: white")

        button.setStyleSheet("color: green")


class TeachersPart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "teacher_part.ui"), self)

        self.t = TeacherLogic(self)
        self.th = TeachersHistoryLogic(self)

        self.stackedWidget.addWidget(self.t)
        self.stackedWidget.addWidget(self.th)

        self.stackedWidget.setCurrentIndex(0)
        self.buttons(self.teacher)

        self.setup()

    def setup(self):
        self.teacher.clicked.connect(self.go_to_teachers)
        self.teacher_history.clicked.connect(self.go_to_history)

    def go_to_teachers(self):
        self.stackedWidget.setCurrentIndex(0)
        self.buttons(self.teacher)

    def go_to_history(self):
        self.stackedWidget.setCurrentIndex(1)
        self.th.setup_tables()
        self.buttons(self.teacher_history)

    def buttons(self, button): 
        self.teacher.setStyleSheet("color: white")
        self.teacher_history.setStyleSheet("color: white")

        button.setStyleSheet("color: green")


class ClassPart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "class_part.ui"), self)

        self.c = ClassesLogic(self)
        self.ce = ClasseleveLogic(self)

        self.stackedWidget.addWidget(self.c)
        self.stackedWidget.addWidget(self.ce)

        self.stackedWidget.setCurrentIndex(0)
        self.buttons(self.classes)

        self.setup()

    def setup(self):    
        self.classes.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.classeleve.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

    def go_to_classes(self):
        self.stackedWidget.setCurrentIndex(0)
        self.c.populate_combos()
        self.buttons(self.classes)

    def go_to_classeleve(self):
        self.stackedWidget.setCurrentIndex(1) 
        self.buttons(self.classeleve)
        self.ce.populate_combo()

    def buttons(self, button):
        self.classes.setStyleSheet("color: white")
        self.classeleve.setStyleSheet("color: white")

        button.setStyleSheet("color: green")

class MoneyPart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "money.ui"), self)

        self.e = EnteryLogic(self)
        self.o = OutMoneyLogic(self)
        self.s = BalanceLogic(self)
        self.c = CaisseLogic(self)
        self.b = BankLogic(self)

        self.stackedWidget.addWidget(self.e)
        self.stackedWidget.addWidget(self.o)
        self.stackedWidget.addWidget(self.s)
        self.stackedWidget.addWidget(self.c)
        self.stackedWidget.addWidget(self.b)

        self.stackedWidget.setCurrentIndex(0)
        self.buttons(self.add_money)


        self.setup()

    def setup(self):
        self.add_money.clicked.connect(self.income)
        self.out_money.clicked.connect(self.expenses)
        self.solde.clicked.connect(self.balance)
        self.caisse.clicked.connect(self.go_to_caisse)
        self.bank.clicked.connect(self.go_to_bank)

    def income(self):
        self.stackedWidget.setCurrentIndex(0)
        self.e.setup_table()
        self.e.populate_combo()
        self.buttons(self.add_money)

    def expenses(self):
        self.stackedWidget.setCurrentIndex(1)
        self.o.setup_table()
        self.o.populate_combo()
        self.buttons(self.out_money)

    def balance(self):
        self.stackedWidget.setCurrentIndex(2)
        self.s.setup_table()
        self.s.populate_combo()  
        self.buttons(self.solde)    

    def go_to_caisse(self):
        self.stackedWidget.setCurrentIndex(3)
        self.c.setup_table()
        self.buttons(self.caisse)   

    def go_to_bank(self):
        self.stackedWidget.setCurrentIndex(4)   
        self.b.setup_table()
        self.buttons(self.bank)

    def buttons(self, button):
        self.add_money.setStyleSheet("color: white")
        self.out_money.setStyleSheet("color: white")
        self.solde.setStyleSheet("color: white")
        self.caisse.setStyleSheet("color: white")
        self.bank.setStyleSheet("color: white")

        button.setStyleSheet("color: green")


class PaymentPart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "payment_part.ui"), self)

        self.ap = AddPayment(self)
        self.vp = ViewPayment()
        self.vnp = ViewNotPayedLogic()

        self.stackedWidget.addWidget(self.ap)
        self.stackedWidget.addWidget(self.vp)
        self.stackedWidget.addWidget(self.vnp)

        self.stackedWidget.setCurrentIndex(0)
        self.buttons(self.add_payment)

        self.setup()

    def setup(self):
        self.add_payment.clicked.connect(self.go_to_add_payment)
        self.view_payment.clicked.connect(self.go_to_view_payment)
        self.view_not_payed.clicked.connect(self.go_to_view_not_payed)

    def go_to_add_payment(self):    
        self.stackedWidget.setCurrentIndex(0)
        self.ap.populate_combo()
        self.buttons(self.add_payment)

    def go_to_view_payment(self):
        self.stackedWidget.setCurrentIndex(1)
        self.vp.populate_combos()
        self.vp.setup_table()
        self.vp.show_students_list()
        self.buttons(self.view_payment)

    def go_to_view_not_payed(self):
        self.stackedWidget.setCurrentIndex(2)
        self.vnp.populate_classes()
        self.buttons(self.view_not_payed)

    def buttons(self, button):
        self.add_payment.setStyleSheet("color: white")
        self.view_payment.setStyleSheet("color: white")
        self.view_not_payed.setStyleSheet("color: white")

        button.setStyleSheet("color: green")


class AbsentsPart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "absents.ui"), self)

        self.at = AddAbscentTLogic(self)
        self.vat = ViewAbsentTeacherLogic(self)
        self.aas = AddAbsentStudentLogic(self)
        self.vs = ViewAbsentStudentLogic(self)

        self.stackedWidget.addWidget(self.at)
        self.stackedWidget.addWidget(self.vat)
        self.stackedWidget.addWidget(self.aas)
        self.stackedWidget.addWidget(self.vs)

        self.stackedWidget.setCurrentIndex(0)
        self.buttons(self.add_teacher)

        self.setup()

    def setup(self):
        self.add_teacher.clicked.connect(self.go_to_add_absent_teacher)
        self.view_teacher.clicked.connect(self.go_to_view_absent_teacher)
        self.add_student.clicked.connect(self.go_to_add_absent_student)
        self.view_student.clicked.connect(self.go_to_view_absent_student)

    def go_to_add_absent_teacher(self):
        self.stackedWidget.setCurrentIndex(0)
        self.at.setup_tabel()
        self.buttons(self.add_teacher)

    def go_to_view_absent_teacher(self):
        self.stackedWidget.setCurrentIndex(1)
        self.vat.populate_class()
        self.vat.setup_table()
        self.buttons(self.view_teacher)

    def go_to_add_absent_student(self):
        self.stackedWidget.setCurrentIndex(2)
        self.aas.setup_student_table()
        self.buttons(self.add_student)

    def go_to_view_absent_student(self):
        self.stackedWidget.setCurrentIndex(3)
        self.vs.populate_class()
        self.vs.setup_table()
        self.buttons(self.view_student)

    def buttons(self, button):
        self.add_teacher.setStyleSheet("color: white")
        self.view_teacher.setStyleSheet("color: white")
        self.add_student.setStyleSheet("color: white")
        self.view_student.setStyleSheet("color: white")

        button.setStyleSheet("color: green")


class UserPart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "user_part.ui"), self)

        self.u = UserLogic(self)
        self.r = RoleLogic(self)

        self.stackedWidget.addWidget(self.u)
        self.stackedWidget.addWidget(self.r)

        self.stackedWidget.setCurrentIndex(0)
        self.buttons(self.user)

        self.setup()

    def setup(self):
        self.user.clicked.connect(self.go_to_users)
        self.add_role.clicked.connect(self.go_to_roles)

    def go_to_users(self):
        self.stackedWidget.setCurrentIndex(0)
        self.u.populate_combo()
        self.buttons(self.user)

    def go_to_roles(self):
        self.stackedWidget.setCurrentIndex(1)
        self.buttons(self.add_role)

    def buttons(self, button):
        self.user.setStyleSheet("color: white")
        self.add_role.setStyleSheet("color: white")

        button.setStyleSheet("color: green")

# THe settings part is added from another file


if __name__ == '__main__':
    app = QApplication([])
    window = PaymentPart()
    window.show()
    app.exec()