from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt6.QtCore import QDate, QPropertyAnimation, QEasingCurve
from .models import Students, ClassEleve, StudentsHistory
from .database import SessionLocal
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from tables_model.students_model import StudentsSearchTableModel, StudentsTableModel, StudentsHistoryTableModel
from os import path
from .help import HelpLogic, Printing


class StudentsLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "students.ui"), self)

        self.identifier = 0
        self.model = None

        self.to.setDate(QDate.currentDate())
        self.date_inscrit.setDate(QDate.currentDate())
        self.gender_search.setCurrentIndex(-1)

        self.animation = QPropertyAnimation(self.search_frame, b"maximumWidth")
        self.animation.setDuration(500)  # 500ms animation
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.search_section("minimize")

        self.setup_table()

        self.setup_ui()

    def setup_ui(self):
        self.new_btn.clicked.connect(self.reset)
        self.add_btn.clicked.connect(lambda: self.controls("add"))
        self.update_btn.clicked.connect(lambda: self.controls("update"))
        self.delete_btn.clicked.connect(lambda: self.security("delete"))
        self.minimize.clicked.connect(lambda: self.search_section("minimize"))
        self.maximize.clicked.connect(lambda: self.search_section("maximize"))
        self.reset_btn.clicked.connect(self.reset_filters)
        self.student_tab.doubleClicked.connect(self.select_student)
        self.search_btn.clicked.connect(self.show_table)
        self.new_year.clicked.connect(lambda: self.security("new_year"))
        self.printing_btn.clicked.connect(self.print_preview)
        self.export_btn.clicked.connect(self.excel)

    def setup_table(self):
        session = SessionLocal()

        self.model = StudentsTableModel(session)

        self.student_tab.setModel(self.model)

    def controls(self, action):
        name = self.name.text()
        parent = self.parent.text()
        num_tel = self.num_tel.text()
        num_tel_2 = self.num_tel_2.text()
        cin = self.cin.text()
        activity = self.activity.currentText()
        excused = self.excused.currentText()
        date = self.date_inscrit.date()

        if action == "add":
            if self.existing(name, parent):
                HelpLogic.error("التلميذ موجود")
                return

        if len(name) == 0:
            HelpLogic.error("خطأ في الإسم")
        elif len(parent) == 0:
            HelpLogic.error("ينقص إسم الولي")
        elif len(cin) != 8 or not cin.isdigit():
            HelpLogic.error("خطأ في رقم ال ب ت و")
        elif len(num_tel) != 8 or not num_tel.isdigit():
            HelpLogic.error("خطأ في رقم الهاتف")
        elif len(num_tel_2) != 8 and len(num_tel_2) != 0:
            HelpLogic.error("خطأ في رقم الهاتف الثاني")
        elif len(num_tel_2) != 0 and not num_tel_2.isdigit():
            HelpLogic.error("خطأ في رقم الهاتف الثاني")
        elif len(activity) == 0:
            HelpLogic.error("اختر النشاط")
        elif len(excused) == 0:
            HelpLogic.error("هل هذا التلميذ معفى")
        else:
            if len(num_tel_2) == 8 and num_tel_2.isdigit():
                num_tel += f"/{num_tel_2}"
            if action == "add":
                self.add_student(name, parent, cin, activity, num_tel, excused, date)
                self.model.refresh()
            else:
                self.update_student()
    
    def add_ensurance(self, student_id, class_name):
        session = SessionLocal()

        ensurance = ClassEleve(student_id=student_id, class_name=class_name)
        try:
            session.add(ensurance)
            session.commit()
        except IntegrityError as e:
            print(e)
            session.rollback()
        finally:
            session.close()

    def add_student(self, name, parent, cin, activity, num_tel, excused, date):
        note = self.note.text()
        gender = self.gender.currentText()
        age = self.birthday.date()
        session = SessionLocal()
        try:
            student = Students()
            student.name=name
            student.birthday=student.set_birthday(age)
            student.parent=parent
            student.cin=cin
            student.activity=activity
            student.num_tel=num_tel
            student.excused=excused
            student.date_inscrit=student.set_date_inscrit(date) 
            student.gender=gender
            student.note=note
            student.user = "Yahia"
            session.add(student)
            session.commit()

            student_id = student.num_inscrit
            if student_id is None:
                print("none")
                return
            self.add_ensurance(student_id, "تأمين")
            self.add_history(student_id, date)

        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()
            self.reset()
            self.setup_table()

    def update_student(self):
        session = SessionLocal()

        student = session.query(Students).filter_by(num_inscrit=self.identifier).first()

        if student is not None:
            try:
                student.name = self.name.text()
                student.birthday = student.set_birthday(self.birthday.date())           
                student.parent = self.parent.text()
                student.cin = self.cin.text()
                student.activity = self.activity.currentText()
                student.num_tel = self.num_tel.text()
                student.excused = self.excused.currentText()
                student.date_inscrit = student.set_date_inscrit(self.date_inscrit.date())
                student.gender = self.gender.currentText()
                student.note = self.note.text()
                session.commit()
            except Exception as e:
                print(e)
                session.rollback()
            finally:
                session.close()
                self.identifier = 0
                self.setup_table()
                self.reset()
                self.reset_filters()
        else:
            HelpLogic.error("هذا التلميذ غير موجود")
            session.close()
         
    def select_student(self):
        row = self.student_tab.selectionModel().selectedRows()
        if not row:
            HelpLogic.error("يرجى تحديد التلميذ")
            return
        
        row_index = row[0].row()
        
        self.identifier = self.model.data(self.model.index(row_index, 0), role=0)
        self.student_tab.clearSelection()
        self.repopulate()

    def repopulate(self):
        session = SessionLocal()

        student = session.query(Students).filter_by(num_inscrit=self.identifier).first()
        session.close()

        if student is not None:	
            self.name.setText(student.name)
            self.birthday.setDate(student.get_birthday())
            self.parent.setText(student.parent)
            self.cin.setText(str(student.cin))
            self.activity.setCurrentText(student.activity)
            self.excused.setCurrentText(student.excused)
            self.date_inscrit.setDate(student.get_date_inscrit())
            self.gender.setCurrentText(student.gender)
            self.note.setText(student.note)
            nums = student.num_tel.split("/")
            self.num_tel.setText(nums[0])
            if len(nums) == 2:
                self.num_tel_2.setText(nums[1])

    def security(self, action):
        msg = QMessageBox()
        if action == "delete":
            text = "متأكد من حذف هذا التلميذ ؟"
            btn = 'حذف'
        else:
            text = "متأكد من تسجيل هذا التلميذ ؟"
            btn = 'تسجيل'

        ret = msg.question(self, btn, text, msg.StandardButton.Yes | msg.StandardButton.No)

        if ret == msg.StandardButton.Yes:
            if action == "delete":
                if self.permenant():
                    self.delete_permanant()
                else:
                    self.delete_student()
            else:
                self.set_new_year()

        self.reset()

        self.setup_table()

    def permenant(self):
        
        session = SessionLocal()
        student = session.query(Students).filter_by(num_inscrit=self.identifier).first()

        if student is not None:
            return student.activity == "غير فاعل"
        
        session.close()
        
    def delete_permanant(self):
        session = SessionLocal()

        student = session.query(Students).filter_by(num_inscrit=self.identifier)

        test = student.first()

        if test is not None:
            try:
                student.delete()
                session.commit()
            except Exception as e :
                print("this is permanent delete 236 \n", e)
                session.rollback()
            finally:
                session.close()
                self.identifier = 0
                self.setup_table()

    def delete_student(self):
        session = SessionLocal()

        student = session.query(Students).filter_by(num_inscrit=self.identifier).first()

        classeleve = session.query(ClassEleve).filter(and_(
            ClassEleve.student_id == self.identifier,
            ClassEleve.class_name != "تأمين"
        ))

        nb = len(classeleve.all()) if classeleve is not None else 0

        if student is not None:
            try:
                student.activity = "غير فاعل"
                if nb > 0:
                    classeleve.delete()
                session.commit()
            except Exception as e :
                print("257 \n", e)
                session.rollback()
                HelpLogic.error("")
            finally:
                session.close()
        else:	
            HelpLogic.error("هذا التلميذ غير موجود.")
            session.close()
        self.identifier = 0
        self.model.refresh()
        self.student_tab.repaint()

    def search_section(self, action):
        if action == "minimize":
            self.animation.setStartValue(200)
            self.animation.setEndValue(0)
        elif action == "maximize":
            self.animation.setStartValue(0)
            self.animation.setEndValue(200)
        else:
            print("not recognized")
        
        self.animation.start()

    def set_new_year(self):
        session = SessionLocal()

        student = session.query(Students).filter_by(num_inscrit=self.identifier).first()

        if student is not None:
            try:
                student.date_inscrit = student.set_date_inscrit(QDate.currentDate())
                session.commit()
                self.add_history(self.identifier, QDate.currentDate())
            except Exception:
                session.rollback()
                HelpLogic.error("هذا التلميذ موجود.")
            finally:
                session.close()
        else:	
            HelpLogic.error("هذا التلميذ غير موجود.")
            session.close()

        self.identifier = 0
        self.model.refresh()
    
    def add_history(self, student_id, date):
        session = SessionLocal()

        th = StudentsHistory()

        th.num_inscrit = student_id
        th.date_inscrit = th.set_date_inscrit(date)
        th.user = "Yahia"

        try:
            session.add(th)
            session.commit()
        except IntegrityError as e:
            print(e)
            session.rollback()
            HelpLogic.error("لم تتم الاضافة")
        finally:
            session.close()

    def reset(self):
        self.name.setText("")
        self.birthday.setDate(QDate.fromString("2000-01-01", "yyyy-MM-dd"))
        self.parent.setText("")
        self.num_tel.setText("")
        self.num_tel_2.setText("")
        self.cin.setText("")
        self.activity.setCurrentText("")
        self.excused.setCurrentText("")
        self.date_inscrit.setDate(QDate.currentDate())

    def reset_filters(self):
        self.search_by_name.setText("")
        self.du.setDate(QDate.fromString("2000-01-01", "yyyy-MM-dd"))
        self.to.setDate(QDate.currentDate())
        self.excused_search.setCurrentIndex(0)
        self.activity_search.setCurrentIndex(0)
        self.gender_search.setCurrentIndex(-1)

    def show_table(self):
        du = self.du.date().toPyDate()
        au = self.to.date().toPyDate()
        excused = self.excused_search.currentText()
        if excused == "":
            excused = None
        activity = self.activity_search.currentText()
        gender = self.gender_search.currentText()
        if gender == "":
            gender = None
        
        name = self.search_by_name.text()
        if name == "":
            name = None

        self.model.refresh(name=name, du=du, au=au, excused=excused, activity=activity, gender=gender)

        self.nb.setText(str(self.model.rowCount()))
        self.student_tab.repaint()

    def print_preview(self):
        try:
            title = "قائمة التلميذ"

            intro = self.model.intro

            header = ["معفى", "رقم الهاتف", "تاريخ الولادة", "الإسم"]

            foot = "المجموع: " + str(self.model.rowCount())

            data = []

            for student in self.model.students:
                row = [
                    student.excused,
                    student.num_tel,
                    student.birthday.strftime("%Y-%m-%d"),
                    student.name
                ]
                data.append(row)
            
            printer = Printing()
            printer.setup_document(data, header, title, intro, foot)
            printer.exec()

        except Exception as e:
            print(e)        
            HelpLogic.error("لا يمكنك الطباعة")

    def excel(self):
        try:
            header = ["معفى", "رقم الهاتف", "تاريخ الولادة", "الإسم"]
            data = []

            for student in self.model.students:
                row = [
                    student.excused,
                    student.num_tel,
                    student.birthday.strftime("%Y-%m-%d"),
                    student.name
                ]
                data.append(row)

            HelpLogic.excel(self, header, data)

        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك تحميل الملف")


    @staticmethod
    def existing(name, parent):
        session = SessionLocal()
        data = session.query(Students).filter_by(name=name, parent=parent).first()
        if data is None:
            return False
        else:
            return True

class StudentsHistoryLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "student_history.ui"), self)

        self.model = None

        self.setup_table()

        self.setup()

    def setup(self):
        self.search_btn.clicked.connect(self.search)
        self.reset_btn.clicked.connect(lambda: self.num_ins_search.setText(""))
        self.printing_btn.clicked.connect(self.print_preview)
        self.export_btn.clicked.connect(self.excel)

    def setup_table(self):
        session = SessionLocal()

        self.model = StudentsHistoryTableModel(session)

        self.student_tab.setModel(self.model)

    def search(self):
        identifier = self.num_ins_search.text()
        
        if identifier == "":
            identifier = None

        self.model.refresh(identifier)

    def print_preview(self):
        try:
            title = "قائمة التلميذ"

            intro = self.model.intro

            header = ["معفى", "رقم الهاتف", 'سنوات الدراسة', "تاريخ الولادة", "الإسم"]

            foot = "المجموع: " + str(self.model.rowCount())

            data = []

            for student in self.model.students:
                row = [
                    student.student.excused,
                    student.student.num_tel,
                    student.date_inscrit.strftime("%Y-%m-%d"),
                    student.student.birthday.strftime("%Y-%m-%d"),
                    student.student.name
                ]
                data.append(row)
            
            printer = Printing()
            printer.setup_document(data, header, title, intro, foot)
            printer.exec()

        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك الطباعة")


    def excel(self):
        try:
            header = ["معفى", "رقم الهاتف", 'سنوات الدراسة', "تاريخ الولادة", "الإسم"]
            data = []

            for student in self.model.students:
                row = [
                    student.student.excused,
                    student.student.num_tel,
                    student.date_inscrit.strftime("%Y-%m-%d"),
                    student.student.birthday.strftime("%Y-%m-%d"),
                    student.student.name
                ]
                data.append(row)

            HelpLogic.excel(self, header, data)

        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك تحميل الملف")

class ClassesPerStudentLogic(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "classes_per_student.ui"), self)

        self.model = None
        self.name = ""

        self.setup_table()
        self.setup()

    def setup(self):
        self.reset_btn.clicked.connect(self.reset)
        self.search_ent.textChanged.connect(self.student_search)
        self.student_list.doubleClicked.connect(self.list_of_classes)

    def setup_table(self):
        session = SessionLocal()

        self.model = StudentsSearchTableModel(session)

        self.student_list.setModel(self.model)

        session.close()

    def student_search(self):
        name = self.search_ent.text()

        self.model.refresh(name)
        self.student_list.repaint()

    def get_id(self):
        row = self.student_list.selectionModel().selectedRows()
        if not row:
            HelpLogic.error("يرجى تحديد التلميذ")
            return
        
        row_index = row[0].row()

        self.name = self.model.data(self.model.index(row_index, 1), role=0)	

        return self.model.data(self.model.index(row_index, 0), role=0)

    def list_of_classes(self):
        id = self.get_id()

        session = SessionLocal()

        classes = session.query(ClassEleve).with_entities(ClassEleve.class_name).filter(ClassEleve.student_id == id, ClassEleve.class_name != "تأمين").all()

        session.close()

        self.class_list.clear()

        if classes:
            for class_name in classes:
                self.class_list.addItem(class_name[0])

        else:
            HelpLogic.error("لا يوجد صفوف لهذا التلميذ")


    def reset(self):
        self.search_ent.setText("")
        self.class_list.clear()

if __name__ == '__main__':
    app = QApplication([])
    window = Students()
    window.show()
    app.exec()