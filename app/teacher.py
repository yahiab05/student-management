from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QDate
from .models import Teachers, Classes, TeachersHistory
from .database import SessionLocal
from os import path
from sqlalchemy.exc import IntegrityError
from tables_model.teacher_model import TeachersTableModel, TeachersHistoryTableModel
from .help import Printing, HelpLogic


class TeacherLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "teacher.ui"), self)

        self.model = None

        self.identifier = 0
        

        self.setup()
        self.setup_table()
        self.show_teachers()
        self.reset()


    def setup(self):
        self.new_btn.clicked.connect(self.reset)
        self.add_btn.clicked.connect(lambda: self.control("add"))
        self.update_btn.clicked.connect(lambda: self.control("update"))
        self.delete_btn.clicked.connect(self.sup_security)
        self.teachers_table.doubleClicked.connect(self.select_row)
        self.search.textChanged.connect(self.show_teachers)
        self.new_year_btn.clicked.connect(self.new_year_security)
        self.printing_btn.clicked.connect(self.printing_preview)
        self.export_btn.clicked.connect(self.excel)

    def setup_table(self):
        session = SessionLocal()

        self.model = TeachersTableModel(session)

        self.teachers_table.setModel(self.model)

        session.close()

    def control(self, action):
        name = self.name.text()
        phone1 = self.phone.text()
        phone2 = self.phone_2.text()

        if len(name) == 0:
            HelpLogic.error("خطأ في الإسم")
        elif len(phone1) != 8 or not phone1.isdigit():
            HelpLogic.error("خطأ في رقم الهاتف")
        elif len(phone2) != 8 and len(phone2) != 0:
            HelpLogic.error("خطأ في رقم الهاتف الثاني")
        elif len(phone2) != 0 and not phone2.isdigit():
            HelpLogic.error("خطأ في رقم الهاتف الثاني")
        else:
            if action == "add":
                self.add()
            else:
                self.update_query()

    def add(self):
        name = self.name.text()
        date_ins = self.date_inscrit.date()
        birthday = self.birthday.date()
        phone1 = self.phone.text()
        phone2 = self.phone_2.text()
        note = self.note.text()
        money = self.money.currentText()

        if len(phone2) == 8 and phone2.isdigit():
            phone1 += f"/{phone2}"

        new_teacher = Teachers()

        new_teacher.name = name
        new_teacher.date_inscrit = new_teacher.set_date_iscrit(date_ins)
        new_teacher.birthday = new_teacher.set_birthday(birthday)
        new_teacher.phone = phone1
        new_teacher.note = note
        new_teacher.payed = money
        new_teacher.user = HelpLogic.get_username()

        session = SessionLocal()
        try:
            session.add(new_teacher)
            session.commit()
            self.setup_table()
            self.add_history(new_teacher.id, date_ins, money)
        except IntegrityError as e:
            print(e)
            session.rollback()
            HelpLogic.error("هذا المعلم موجود.")
        finally:
            session.close()
            self.show_teachers()
            self.reset()
            

    def update_query(self):
        name = self.name.text()
        date_ins = self.date_inscrit.date()
        birthday = self.birthday.date()
        phone1 = self.phone.text()
        phone2 = self.phone_2.text()
        note = self.note.text()
        money = self.money.currentText()

        if len(phone2) == 8 and phone2.isdigit():
            phone1 += f"/{phone2}"

        session = SessionLocal()
        teacher = session.query(Teachers).filter(Teachers.id == self.identifier).first()
        if teacher is not None:
            try:
                teacher.name = name
                teacher.date_inscrit = teacher.set_date_iscrit(date_ins)
                teacher.birthday = teacher.set_birthday(birthday)
                teacher.phone = phone1
                teacher.note = note
                teacher.payed = money
                teacher.user = "Yahia"
                session.commit()
            except IntegrityError:
                session.rollback()
                self.error("هذا المعلم موجود.")
            finally:
                session.close()
                self.show_teachers()
        else:
            self.error("هذا المعلم غير موجود.")
            session.close()

        self.reset()

    def sup_security(self):
        msg = QMessageBox()
        ret = msg.question(self, 'حذف', "متأكد من حذف هذا الأستاذ؟", msg.StandardButton.Yes | msg.StandardButton.No)

        if ret == msg.StandardButton.Yes:
            self.delete()
        else:
            self.reset()
            self.search.setText("")

    def delete(self):
        session = SessionLocal()
        teacher = session.query(Teachers).filter(Teachers.id == self.identifier).first()
        if teacher is not None:
            if self.has_classes(teacher.name):
                HelpLogic.error("هذا المعلم لديه فصل")
            else:
                try:
                    session.delete(teacher)
                    session.commit()
                except Exception:
                    session.rollback()
                    HelpLogic.error("هذا المعلم موجود.")
                finally:
                    session.close()
                    self.setup_table()
        else:	
            HelpLogic.error("هذا المعلم غير موجود.")
            session.close()

        self.reset()

    def has_classes(self, name):
        session = SessionLocal()
        data = session.query(Classes).filter(Classes.teacher == name).first()

        session.close()
        if data is None:
            return False
        
        return True

    def reset(self):
        self.name.setText("")
        self.date_inscrit.setDate(QDate.currentDate())
        self.birthday.setDate(QDate.currentDate())
        self.phone.setText("")
        self.phone_2.setText("")
        self.note.setText("")

        self.identifier = 0

    def select_row(self):
        row = self.teachers_table.selectionModel().selectedRows()
        if not row:
            HelpLogic.error("يرجى تحديد قسم")
            return
        
        row_index = row[0].row()
        
        self.identifier = self.model.data(self.model.index(row_index, 0), role=0)
        self.repopulate()

    def repopulate(self):
        session = SessionLocal()

        data = session.query(Teachers).filter(Teachers.id == self.identifier).first()

        if data is not None:
            self.name.setText(data.name)
            self.date_inscrit.setDate(data.get_date_inscrit())
            self.birthday.setDate(data.get_birthday())
            if len(data.phone) > 8:
                phones = data.phone.split("/")
                self.phone.setText(phones[0])
                self.phone_2.setText(phones[1])
            else:
                self.phone.setText(data.phone)
            self.note.setText(data.note)
            self.money.setCurrentText(data.payed)

    def show_teachers(self):
        name = self.search.text()

        if name == "":
            name = None
        
        self.model.refresh(name)

        self.nb.setText(str(self.model.rowCount()))

    def new_year_security(self):
        if self.identifier != 0:
            msg = QMessageBox()
            ret = msg.question(None, 'تسجيل', "هل تريد تسجيل هذا المعلم؟", msg.StandardButton.Yes | msg.StandardButton.No)

            if ret == msg.StandardButton.Yes:
                self.add_history(self.identifier, self.date_inscrit.date(), self.money.currentText())
                self.new_year(self.identifier)
        self.reset()
        self.show_teachers()

    def new_year(self, teacher_id):
        session = SessionLocal()
        teacher = session.query(Teachers).filter(Teachers.id == teacher_id).first()
        if teacher is not None:
            try:
                teacher.date_inscrit = teacher.set_date_iscrit(QDate.currentDate())
                session.commit()
            except IntegrityError:
                session.rollback()
                HelpLogic.error("هذا المعلم موجود.")
            finally:
                session.close()
                self.show_teachers()
        else:
            HelpLogic.error("هذا المعلم غير موجود.")
            session.close()

    def add_history(self, teacher_id, date, payed):
        session = SessionLocal()

        th = TeachersHistory()

        th.teacher_id = teacher_id
        th.date_inscrit = th.set_date_inscrit(date)
        th.payed = payed    
        th.user = HelpLogic.get_username()

        try:
            session.add(th)
            session.commit()
        except IntegrityError:
            session.rollback()
            HelpLogic.error("لم تتم الاضافة")
        finally:
            session.close()

    def printing_preview(self):
        try:

            title = "قائمة الأساتذة"

            headers = ["رقم الهاتف", "تاريخ الولادة", "الإسم"]

            foot = "المجموع: " + str(self.model.rowCount())

            data = []

            for teacher in self.model.teachers:
                row = [
                    str(teacher.phone),
                    teacher.birthday.strftime("%Y-%m-%d"),
                    teacher.name
                ]
                data.append(row)

            printer = Printing()
            printer.setup_document(data, headers, title, "", foot)

            printer.exec()

        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك الطباعة")

    def excel(self):
        try: 
            headers = ["رقم الهاتف", "تاريخ الولادة", "الإسم"]
            data = []

            for teacher in self.model.teachers:
                row = [
                    teacher.phone,
                    teacher.birthday.strftime("%Y-%m-%d"),
                    teacher.name
                ]
                data.append(row)

            HelpLogic.excel(self, headers, data)
        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك تحميل الملف")


class TeachersHistoryLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "teacher_history.ui"), self)

        self.model = None

        self.setup_tables()
        self.setup()


    def setup(self):
        self.search_btn.clicked.connect(lambda: self.show_table(self.search.text()))
        self.reset_btn.clicked.connect(lambda: self.search.setText(""))
        self.printing_btn.clicked.connect(self.printing_preview)
        self.export_btn.clicked.connect(self.excel)

    def setup_tables(self):
        session = SessionLocal()

        self.model = TeachersHistoryTableModel(session)

        self.history_table.setModel(self.model)

        session.close()

    def show_table(self, teacher_id=None):
        if teacher_id == "": teacher_id = None
        if teacher_id is not None:

            self.model.refresh(teacher_id)

        self.nb.setText(str(self.model.rowCount()))

    def printing_preview(self):
        try:

            title = "قائمة الأساتذة"

            headers = ["تاريخ الولادة", "سنوات التدريس", "الإسم", "رقم التسجيل"]

            foot = f"""عدد الأساتذة: {self.model.rowCount()}"""

            data = []

            for teacher in self.model.teachers:
                row = [
                    teacher.teacher.birthday.strftime("%Y-%m-%d"),
                    teacher.date_inscrit.strftime("%Y-%m-%d"),
                    teacher.teacher.name,
                    teacher.teacher_id
                ]
                data.append(row)

            printer = Printing()
            printer.setup_document(data, headers, title, "", foot)

            printer.exec()

        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك الطباعة")

    def excel(self):
        try:
            headers = ["تاريخ الولادة", "سنوات التدريس", "الإسم", "رقم التسجيل"]
            data = []

            for teacher in self.model.teachers:
                row = [
                    teacher.teacher.birthday.strftime("%Y-%m-%d"),
                    teacher.date_inscrit.strftime("%Y-%m-%d"),
                    teacher.teacher.name,
                    teacher.teacher_id
                ]
                data.append(row)

            HelpLogic.excel(self, headers, data)
        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك تحميل الملف")

    
