from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QDate, QTime
from .help import HelpLogic, Printing
from .database import SessionLocal
from .models import AbsentS, ClassEleve, Students
from tables_model.students_model import StudentsSearchTableModel
from tables_model.abscent_models import AbsentStudentTableModel
from sqlalchemy.orm import joinedload
from os import path

class AddAbsentStudentLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "add_absents_s.ui"), self)

        self.identifier = 0

        self.setup_student_table()
        self.reset()
        self.setup()

    def setup(self):
        self.new_btn.clicked.connect(self.reset)
        self.add_btn.clicked.connect(self.control)
        self.search_ent.textChanged.connect(self.search_student)
        self.student_list.doubleClicked.connect(self.select_student)

    def control(self):
        name = self.name.text()
        classe = self.classroom.currentText()
        date_ab = self.date_ab.date()
        du = self.du_time.time()
        to = self.to_time.time()

        if name == "":
            self.error("الإسم ضروري")
        elif classe == '': 
            self.error("القسم ضروري")
        elif self.unique(name, classe, date_ab, du, to):
            self.error("هذا الغياب موجود")
        else:            
            self.add(classe, date_ab, du, to)

    def add(self, classe, date_ab, du, to):
        session = SessionLocal()

        try:
            new_absent = AbsentS()

            new_absent.num_inscrit = self.identifier
            new_absent.class_ab = classe
            new_absent.date_ab = new_absent.set_date(date_ab)
            new_absent.du = new_absent.set_time(du)
            new_absent.time_last = new_absent.set_time(to)
            new_absent.user = HelpLogic.get_username()

            session.add(new_absent)
            session.commit()
            HelpLogic.error("تمت اضافة الغياب بنجاح")
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()
            self.reset()

    def reset(self):
        self.identifier = 0

        self.name.setText("")
        self.classroom.setCurrentIndex(-1)
        self.date_ab.setDate(QDate.currentDate())
        self.du_time.setTime(QTime(0,0,0))
        self.to_time.setTime(QTime(0,0,0))

    def populate_class(self, identifier):
        session = SessionLocal()

        classes = session.query(ClassEleve).with_entities(ClassEleve.class_name).filter(ClassEleve.student_id == identifier, ClassEleve.class_name != "تأمين").all()

        self.classroom.clear()

        for class_name in classes:
            self.classroom.addItem(class_name[0])

        session.close()

        self.classroom.setCurrentIndex(-1)
        

    def setup_student_table(self):
        session = SessionLocal()

        self.model = StudentsSearchTableModel(session)

        self.student_list.setModel(self.model)

        session.close()

    def search_student(self):
        name = self.search_ent.text()

        self.model.refresh(name)
        self.student_list.repaint()

    def select_student(self):
        row = self.student_list.selectionModel().selectedRows()
        if not row:
            HelpLogic.error("يرجى تحديد التلميذ")
            return
        
        row_index = row[0].row()    

        self.identifier = self.model.data(self.model.index(row_index, 0), role=0)
        name = self.model.data(self.model.index(row_index, 1), role=0)

        self.student_list.clearSelection()

        self.name.setText(str(name))
        self.populate_class(self.identifier)

    @staticmethod
    def unique(num_inscrit, classroom, date_ab, du, to): 
        session = SessionLocal()

        ab = session.query(AbsentS).filter(AbsentS.num_inscrit == num_inscrit, AbsentS.class_ab == classroom, 
                                           AbsentS.date_ab == date_ab.toPyDate(), AbsentS.du == du.toPyTime(), 
                                           AbsentS.time_last == to.toPyTime()).first()
        
        session.close()

        if ab:
            return True
        else:
            return False
        

class ViewAbsentStudentLogic(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "view_absents_s.ui"), self)

        self.model = None
        self.identififer = 0

        self.setup_table()
        self.reset()
        self.populate_class()
        self.search_student()
        self.setup()

    def setup(self):
        self.search_btn.clicked.connect(self.show_table)
        self.reset_btn.clicked.connect(self.reset)
        self.tbl.doubleClicked.connect(self.line_to_delete)
        self.student_list.itemDoubleClicked.connect(self.select_student)
        self.search_ent.textChanged.connect(self.search_student)
        self.printing_btn.clicked.connect(self.printing_preview)
        self.export_btn.clicked.connect(self.excel)

    def setup_table(self):
        session = SessionLocal()

        self.model = AbsentStudentTableModel(session)

        self.tbl.setModel(self.model)

        session.close()

    def show_table(self):
        name = self.search_ent.text() if self.search_ent.text() != "" else None
        classroom = self.classroom.currentText() if self.classroom.currentText() != "" else None
        from_date = self.du.date().toPyDate()
        to_date = self.to.date().toPyDate()

        self.model.refresh(name, classroom, from_date, to_date)
        self.tbl.repaint()

        self.nb.setText(str(self.model.rowCount()))

    def reset(self):
        self.search_ent.setText("")
        self.classroom.setCurrentIndex(-1)
        self.du.setDate(QDate(2000, 1, 1))
        self.to.setDate(QDate.currentDate())

    def search_student(self):
        name = self.search_ent.text()

        session = SessionLocal()

        teachers =(
    session.query(Students).with_entities(Students.name)
    .join(AbsentS, Students.num_inscrit == AbsentS.num_inscrit).distinct().filter(Students.name.contains(name))
    .all()
)

        session.close()

        self.student_list.clear()
        if teachers is not None:
            for t in teachers:
                self.student_list.addItem(t[0])

    def select_student(self):
        name = self.student_list.currentItem().text()

        self.search_ent.setText(name)

    def populate_class(self):
        session = SessionLocal()

        classes = session.query(AbsentS).with_entities(AbsentS.class_ab).distinct().all()

        self.classroom.clear()

        for class_name in classes:
            self.classroom.addItem(class_name[0])

        session.close() 

        self.classroom.setCurrentIndex(-1)

    def line_to_delete(self):
        row = self.tbl.selectionModel().selectedRows()

        if not row:
            HelpLogic.error("يرجى تحديد الغياب")
            return

        row_index = row[0].row()    
        line = self.model.data(self.model.index(row_index, 0), role=0)

        self.sup_security(line)

    def sup_security(self, line):
        msg = QMessageBox()
        ret = msg.question(self, 'حذف', "متاءكد من حذف هذا الغياب؟", msg.StandardButton.Yes | msg.StandardButton.No)

        if ret == msg.StandardButton.Yes:
            self.delete_ab(line)

    def delete_ab(self, line):
        session = SessionLocal()

        try:
            ab = session.query(AbsentS).filter(AbsentS.id == line).first()
            session.delete(ab)
            session.commit()
            HelpLogic.error("تم حذف الغياب بنجاح")
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()
            self.setup_table()

    def printing_preview(self):
        try:

            title = "قائمة الغياب"

            headers = ["رقم الهاتف", "تاريخ الغياب", "القسم", "الإسم"]

            foot = "المجموع: " + str(self.model.rowCount())

            data = []

            for absent in self.model.absents:
                row = [
                    str(absent.student.num_tel),
                    absent.date_ab.strftime("%Y-%m-%d"),
                    absent.class_ab,
                    str(absent.student.name)
                ]
                data.append(row)

            printer = Printing()
            printer.setup_document(data, headers, title, self.model.intro, foot)

            printer.exec()

        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك الطباعة")

    def excel(self):
        try: 
            headers = ["رقم الهاتف", "تاريخ الغياب", "القسم", "الإسم"]
            data = []

            for absent in self.model.absents:
                row = [
                    str(absent.student.num_tel),
                    absent.date_ab.strftime("%Y-%m-%d"),
                    absent.class_ab,
                    str(absent.student.name)
                ]
                data.append(row)

            HelpLogic.excel(self, headers, data)
        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك تحميل الملف")