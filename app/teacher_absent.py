from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QDate, QTime
from .help import HelpLogic, Printing
from .database import SessionLocal
from .models import AbsentT, Classes, Teachers
from tables_model.abscent_models import AbsentTeacherTableModel
from tables_model.teacher_model import TeacherSearchTableModel
from os import path


class AddAbscentTLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "add_absents_t.ui"), self)

        self.model = None
        self.identifier = 0


        self.setup_tabel()
        self.reset()
        self.setup()

    def setup(self):
        self.add_btn.clicked.connect(self.contol)
        self.new_btn.clicked.connect(self.reset)
        self.search_ent.textChanged.connect(self.search_student)
        self.student_list.doubleClicked.connect(self.select_teacher)

    def setup_tabel(self):
        session = SessionLocal()

        self.model = TeacherSearchTableModel(session)

        self.student_list.setModel(self.model)   

        session.close()

    def search_student(self, name = None):
        self.model.refresh(name)
        self.student_list.repaint()

    def contol(self):
        name = self.name.text()
        classe = self.classroom.currentText()
        date_ab = self.date_ab.date()
        du = self.du_time.time()
        to = self.to_time.time()
        rep = self.replacment.text()

        if rep == "":
            date_rep = None
        else:
            date_rep = self.date_rep.date()

        if name == "":
            self.error("الإسم ضروري")
        elif classe == '':
            self.error("القسم ضروري")
        elif self.unique(name, classe, date_ab, du, to):
            self.error("هذا الغياب موجود")
        else:            
            self.add(name, classe, date_ab, du, to, rep, date_rep)

    def add(self, name, classe, date_ab, du, to, rep, date_rep):
        session = SessionLocal()

        try:
            new_absent = AbsentT()

            new_absent.num_inscrit = self.identifier
            new_absent.class_ab = classe
            new_absent.date_ab = new_absent.set_date(date_ab)
            new_absent.du = new_absent.set_time(du)
            new_absent.time_last = new_absent.set_time(to)
            new_absent.rep = rep
            new_absent.date_rep = None if date_rep == None else new_absent.set_date(date_rep)
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
        self.classroom.clear()
        self.date_ab.setDate(QDate.currentDate())
        self.du_time.setTime(QTime(0,0,0))
        self.to_time.setTime(QTime(0,0,0))
        self.replacment.setText("")
        self.date_rep.setDate(QDate.currentDate())

    def select_teacher(self):
        row = self.student_list.selectionModel().selectedRows()

        if not row:
            HelpLogic.error("يرجى تحديد التلميذ")
            return
        
        row_index = row[0].row()    

        identifier = self.model.data(self.model.index(row_index, 0), role=0)
        name = self.model.data(self.model.index(row_index, 1), role=0)

        self.rep_or_not(name, identifier)

    def rep_or_not(self, name, ID):
        if self.name.text():
            self.replacment.setText(name)
        else:
            self.name.setText(name)
            self.identifier = ID
            self.populate_class(name)

    @staticmethod
    def unique(num_inscrit, classroom, date_ab, du, to): 
        session = SessionLocal()

        ab = session.query(AbsentT).filter(AbsentT.num_inscrit == num_inscrit, AbsentT.class_ab == classroom, 
                                           AbsentT.date_ab == date_ab.toPyDate(), AbsentT.du == du.toPyTime(), 
                                           AbsentT.time_last == to.toPyTime()).first()
        
        session.close()

        if ab:
            return True
        else:
            return False
        
    def populate_class(self, name):
        session = SessionLocal()

        classes = session.query(Classes).filter(Classes.teacher == name).all()
        
        self.classroom.clear()

        if classes is not None:
            for c in classes:
                self.classroom.addItem(c.name)

        self.classroom.setCurrentIndex(-1)

        session.close()


class ViewAbsentTeacherLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "view_absents_t.ui"), self)

        self.setup_table()
        self.populate_class()
        self.teacher_search()
        self.reset()
        self.setup()

    def setup(self):
        self.search_btn.clicked.connect(self.show_table)
        self.reset_btn.clicked.connect(self.reset)
        self.tbl.doubleClicked.connect(self.line_to_delete)
        self.teacher_list.itemDoubleClicked.connect(self.select_teacher)
        self.search_ent.textChanged.connect(self.teacher_search)
        self.printing_btn.clicked.connect(self.printing_preview)
        self.export_btn.clicked.connect(self.excel)

    def setup_table(self):
        session = SessionLocal()

        self.model = AbsentTeacherTableModel(session)

        self.tbl.setModel(self.model)

        session.close()

    def show_table(self):
        name = self.search_ent.text() if self.search_ent.text() != "" else None
        classroom = self.classroom.currentText() if self.classroom.currentText() != "" else None
        rep = self.replacement.currentText() if self.replacement.currentText() != "" else None
        from_date = self.du.date().toPyDate()
        to_date = self.to.date().toPyDate()

        self.model.refresh(name, classroom, rep, from_date, to_date)
        self.tbl.repaint()

        self.nb.setText(str(self.model.rowCount()))

    def reset(self):
        self.search_ent.setText("")
        self.classroom.setCurrentIndex(-1)
        self.replacement.setCurrentIndex(-1)
        self.du.setDate(QDate(2000, 1, 1))
        self.to.setDate(QDate.currentDate())

    def populate_class(self):
        session = SessionLocal()

        classes = session.query(AbsentT).with_entities(AbsentT.class_ab).distinct().all()
        reps = session.query(AbsentT).with_entities(AbsentT.rep).filter(AbsentT.rep != "").distinct().all()
        
        self.classroom.clear()
        self.replacement.clear()

        if classes is not None:
            for c in classes:
                self.classroom.addItem(c[0])

        if reps is not None:
            for r in reps:
                self.replacement.addItem(r[0])

        self.classroom.setCurrentIndex(-1)
        self.replacement.setCurrentIndex(-1)

        session.close()

    def sup_security(self, line):
        msg = QMessageBox()
        ret = msg.question(self, 'حذف', "متأكد من حذف هذا الغياب؟", msg.StandardButton.Yes | msg.StandardButton.No)

        if ret == msg.StandardButton.Yes:
            self.delete_ab(line)

    def delete_ab(self, line):
        session = SessionLocal()

        try:
            ab = session.query(AbsentT).filter(AbsentT.id == line).first()
            session.delete(ab)
            session.commit()
            HelpLogic.error("تم حذف الغياب بنجاح")
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()
            self.setup_table()

    def line_to_delete(self):
        row = self.tbl.selectionModel().selectedRows()

        if not row:
            HelpLogic.error("يرجى تحديد الغياب")
            return

        row_index = row[0].row()    
        line = self.model.data(self.model.index(row_index, 0), role=0)

        print(line)
        self.sup_security(line)
    
    def teacher_search(self):
        name = self.search_ent.text()

        session = SessionLocal()

        teachers =(
    session.query(Teachers).with_entities(Teachers.name)
    .join(AbsentT, Teachers.id == AbsentT.num_inscrit).distinct().filter(Teachers.name.contains(name))
    .all()
)

        session.close()

        self.teacher_list.clear()
        if teachers is not None:
            for t in teachers:
                self.teacher_list.addItem(t[0])

    def select_teacher(self):
        name = self.teacher_list.currentItem().text()

        self.search_ent.setText(name)

    def printing_preview(self):
        try:

            title = "قائمة الغياب"

            headers = ["المعوض", "رقم الهاتف", "تاريخ الغياب", "القسم", "الإسم"]

            foot = f"""عدد الغيبات: {self.model.rowCount()}"""

            data = []

            for absent in self.model.absents:
                row = [
                    absent.rep,
                    absent.teacher.phone,
                    absent.date_ab.strftime("%Y-%m-%d"),
                    absent.class_ab, 
                    absent.teacher.name
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
            headers = ["المعوض", "رقم الهاتف", "تاريخ الغياب", "القسم", "الإسم"]
            data = []

            for absent in self.model.absents:
                row = [
                    absent.rep,
                    absent.teacher.phone,
                    absent.date_ab.strftime("%Y-%m-%d"),
                    absent.class_ab, 
                    absent.teacher.name
                ]
                data.append(row)

            HelpLogic.excel(self, headers, data)
        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك تحميل الملف")
