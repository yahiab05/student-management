from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem
from sqlalchemy.exc import IntegrityError
from .help import HelpLogic
from .models import Users, Role
from .database import SessionLocal
from os import path


class UserLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "user.ui"), self)

        self.show_users()
        self.populate_combo()
        self.setup()

    def setup(self):
        self.new_btn.clicked.connect(self.reset)
        self.add_btn.clicked.connect(lambda: self.control("add"))
        self.update_btn.clicked.connect(lambda: self.control("update"))
        self.delete_btn.clicked.connect(self.sup_security)
        self.tbl.clicked.connect(self.select_user)

    def reset(self):
        self.user.setText('')
        self.passwd.setText('')
        self.role.setCurrentIndex(-1)

    def control(self, action):
        username = self.user.text()
        password = self.passwd.text()
        role = self.role.currentText()

        if username == '':
            HelpLogic.error("إسم المستخدم ضروري")
        elif password == '':
            HelpLogic.error("كلمة السر ضرورية")
        elif role == '':
            HelpLogic.error("وظيفة المستخدم ضرورية")
        else:
            if action == "add":
                self.add(username , password, role)
            else:
                self.update(username, password, role)
            self.reset()

    def add(self, username, password, role):
        session = SessionLocal()

        try:
            new_user = Users(username=username, password=password, role_name=role)
            session.add(new_user)
            session.commit()
            HelpLogic.error('تم إنشاء الحساب بنجاح')
        except Exception as e:
            print(e)
            session.rollback()
            HelpLogic.error("هذا المستخدم موجود")
        finally:
            session.close()
            self.show_users()
    
    def select_user(self):
        row = self.tbl.currentRow()
        self.identifier = self.tbl.item(row, 3).text()

        user = self.tbl.item(row, 0).text()
        password = self.tbl.item(row, 1).text()
        role = self.tbl.item(row, 2).text()

        self.user.setText(user)
        self.passwd.setText(password)
        self.role.setCurrentText(role)

    def sup_security(self):
        msg = QMessageBox()
        ret = msg.question(self, 'حذف', "متأكد من حذف هذا المستخدم ؟", msg.StandardButton.Yes | msg.StandardButton.No)

        if ret == msg.StandardButton.Yes:
            self.delete()

    def delete(self):
        session = SessionLocal()

        user = session.query(Users).filter(Users.id == self.identifier)

        if user is not None:
            try:
                user.delete()
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
            finally:
                session.close()
                self.show_users()
                self.identifier = 0
                self.reset()
        else:
            HelpLogic.error("هذا المستخدم غير موجود")
            session.close()
            self.identifier = 0

    def update(self, username, password, role):
        session = SessionLocal()

        user = session.query(Users).filter(Users.id == self.identifier).first()

        if user is not None:
            try:
                user.username = username
                user.password = password
                user.role_name = role
                session.commit()
            except IntegrityError as e:    
                session.rollback()
                print(e)
                HelpLogic.error("هذا المستخدم موجود")
            finally:
                session.close()
                self.reset()
                self.identifier = 0
                self.show_users()
        else:
            HelpLogic.error("هذا المستخدم غير موجود")
            session.close()
            self.identifier = 0
            self.reset()

    def show_users(self):
        session = SessionLocal()

        users = session.query(Users).all()

        session.close()

        self.tbl.setRowCount(len(users))

        for i in range(len(users)):
            user = users[i]
            self.tbl.setItem(i, 0, QTableWidgetItem(user.username))
            self.tbl.setItem(i, 1, QTableWidgetItem(user.password))
            self.tbl.setItem(i, 2, QTableWidgetItem(user.role_name))
            self.tbl.setItem(i, 3, QTableWidgetItem(str(user.id)))

    def populate_combo(self):
        session = SessionLocal()

        roles = session.query(Role).with_entities(Role.name).all()

        session.close()

        self.role.clear()

        for role in roles:
            self.role.addItem(role[0])

        self.role.setCurrentIndex(-1)

class RoleLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "role.ui"), self)

        self.name_selected = ""
        self.populate_combo()

        self.setup()

    def setup(self):
        self.search_btn.clicked.connect(self.select_role)
        self.reset_btn.clicked.connect(self.reset)
        self.new_btn.clicked.connect(self.reset)
        self.add_btn.clicked.connect(lambda: self.control("add"))
        self.update_btn.clicked.connect(lambda: self.control("update"))
        self.delete_btn.clicked.connect(self.sup_security)
        self.all_btn.clicked.connect(self.select_deselect_all)

    def control(self, action):
        role = self.name.text()
        students = self.students.isChecked()
        teachers = self.teachers.isChecked()
        classes = self.classes.isChecked()
        payment = self.payment.isChecked()
        absents = self.absents.isChecked()
        money = self.money.isChecked()
        settings = self.settings.isChecked()
        user = self.user.isChecked()
        payment_edit = self.payment_edit.isChecked()

        if action == "add":
            self.add(role, students, teachers, classes, payment, absents, money, settings, user, payment_edit)
        else:
            if self.name_selected :
                self.update(students, teachers, classes, payment, absents, money, settings, user, payment_edit)
            else:
                HelpLogic.error("يرجى تحديد دور")

    def add(self, role, students, teachers, classes, payment, absents, money, settings, user, payment_edit):
        session = SessionLocal()

        try:
            new_role = Role(name=role, students=students, teachers=teachers, classes=classes, payment=payment, absent=absents, 
                            money=money, settings=settings, user=user, payment_editting=payment_edit)
            session.add(new_role)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            print(e)
            HelpLogic.error("هذا الدور موجود")
        finally:
            session.close()
            self.reset()
            self.populate_combo()

    def select_role(self):
        if self.name_search.currentText():
            self.name_selected = self.name_search.currentText()

            session = SessionLocal()

            role = session.query(Role).filter(Role.name == self.name_selected).first()

            session.close()

            self.students.setChecked(role.students)
            self.teachers.setChecked(role.teachers)
            self.classes.setChecked(role.classes)
            self.payment.setChecked(role.payment)
            self.absents.setChecked(role.absent)
            self.money.setChecked(role.money)
            self.settings.setChecked(role.settings)
            self.user.setChecked(role.user)
            self.payment_edit.setChecked(role.payment_editting)

    def update(self, students, teachers, classes, payment, absents, money, settings, user, payment_edit):
        session = SessionLocal()

        role = session.query(Role).filter(Role.name == self.name_selected).first()

        role.students = students
        role.teachers = teachers
        role.classes = classes
        role.payment = payment
        role.absent = absents
        role.money = money
        role.settings = settings
        role.user = user
        role.payment_editting = payment_edit

        session.commit()
        session.close()

        self.reset()

    def sup_security(self):
        if self.name_selected:
            msg = QMessageBox()
            ret = msg.question(self, 'حذف', "متأكد من حذف هذا الدور؟", msg.StandardButton.Yes | msg.StandardButton.No)

            if ret == msg.StandardButton.Yes:
                self.delete()

    def delete(self):
        session=SessionLocal()

        role = session.query(Role).filter(Role.name == self.name_selected)

        try:
            role.delete()
            session.commit()
        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكن حذف هذا الدور")
            session.rollback()
        finally:
            session.close()
            self.reset()
            self.populate_combo()       

    def populate_combo(self):
        session = SessionLocal()

        roles = session.query(Role).with_entities(Role.name).all()

        session.close()

        self.name_search.clear()

        for role in roles:
            self.name_search.addItem(role[0])

        self.name_search.setCurrentIndex(-1)

    def reset(self):
        self.name_selected = ""
        self.name.setText("")
        self.name_search.setCurrentIndex(-1)
        self.students.setChecked(False)
        self.teachers.setChecked(False)
        self.classes.setChecked(False)
        self.payment.setChecked(False)
        self.absents.setChecked(False)
        self.money.setChecked(False)
        self.settings.setChecked(False)
        self.user.setChecked(False)
        self.payment_edit.setChecked(False)

    def select_deselect_all(self):
        self.students.setChecked(True)
        self.teachers.setChecked(True)
        self.classes.setChecked(True)
        self.payment.setChecked(True)
        self.absents.setChecked(True)
        self.money.setChecked(True)
        self.settings.setChecked(True)
        self.user.setChecked(True)
        self.payment_edit.setChecked(True)
 


        