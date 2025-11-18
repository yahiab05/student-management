from os import path
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication
from .models import Classes, Teachers, Settings, ClassEleve
from .database import SessionLocal
from tables_model.classes_model import ClassesTableModel, ClasseleveTableModel
from tables_model.students_model import StudentsSearchTableModel
from sqlalchemy.exc import IntegrityError
from .help import HelpLogic, Printing

class ClassesLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "classes.ui"), self)

        self.model = None

        self.identifier = 0

        self.setup()
        self.set_table()
        self.populate_combos()


    def set_table(self):
        session = SessionLocal()
        self.model = ClassesTableModel(session)
        self.class_table.setModel(self.model)
        session.close()


    def setup(self):
        self.new_btn.clicked.connect(self.reset)
        self.add_btn.clicked.connect(lambda: self.control("add"))
        self.update_btn.clicked.connect(lambda: self.control("update"))
        self.delete_btn.clicked.connect(self.sup_security)
        self.class_table.doubleClicked.connect(self.select_row)
        self.search.textChanged.connect(self.show_class)
        self.teacher_search.currentTextChanged.connect(self.show_class)
        self.printing_btn.clicked.connect(self.printing_preview)
        self.export_btn.clicked.connect(self.excel)

    def control(self, action):
        name = self.name.text()
        way = self.way.currentText()
        teacher = self.teacher.currentText()
        note = self.note.text()
        price = self.price.text()
        exchange = self.in_exchange.currentText()
        teacher_part = self.teacher_price.value()
        seance = self.seance.value()

        if action == "add":
            if self.check(name):
                HelpLogic.error("هذا القسم موجود")
                return
        if len(name) == 0:
            HelpLogic.error("خطأ في الإسم")
        elif len(way) == 0:
            HelpLogic.error("خطأ في الطريقة")
        elif len(teacher) == 0:
            HelpLogic.error("ينقص إسم الأستاذ")
        elif len(price) == 0 or not self.is_float(price):
            HelpLogic.error("الثمن يتكون من أرقام")
        elif teacher_part == 0.0 or not self.is_float(teacher_part):
            HelpLogic.error("تحديد حصة المؤدب ضرورية")
        elif seance == 0:
            HelpLogic.error("تحديد عدد الحصص في السنة ضروري")
        else:
            if action == "add":
                self.add_classe(name, way, teacher, note, price, exchange, teacher_part, seance)
            else:
                self.update_class()

    def add_classe(self, name, way, teacher, note, price, exchange, teacher_part, seance):
        session = SessionLocal()
        new_class = Classes(name=name, way=way, teacher=teacher, note=note, price=price, exchange=exchange, 
                            teacher_part=teacher_part, seance=seance, user = HelpLogic.get_username())
        session.add(new_class)
        session.commit()

        self.reset()
        self.set_table()
        self.class_table.repaint()
        self.populate_combos()
        session.close()



    def select_row(self):
        row = self.class_table.selectionModel().selectedRows()
        if not row:
            HelpLogic.error("يرجى تحديد قسم")
            return
        
        row_index = row[0].row()    

        self.identifier = self.model.data(self.model.index(row_index, 0), role=0)

        self.repopulate()

    def repopulate(self):
        session = SessionLocal()

        data = session.query(Classes).filter(Classes.id == self.identifier).first()

        session.close()

        if data is not None:
            self.name.setText(data.name)
            self.way.setCurrentText(data.way)
            self.teacher.setCurrentText(data.teacher)
            self.note.setText(data.note)
            self.price.setText(str(data.price))
            self.in_exchange.setCurrentText(data.exchange)
            self.teacher_price.setValue(data.teacher_part)
            self.seance.setValue(data.seance)

    def update_class(self):
        session = SessionLocal()

        course = session.query(Classes).filter(Classes.id == self.identifier).first()

        if course is not None:
            course.name = self.name.text()
            course.way = self.way.currentText()
            course.teacher = self.teacher.currentText()
            course.note = self.note.text()
            course.price = self.price.text()
            course.exchange = self.in_exchange.currentText()
            course.teacher_part = self.teacher_price.value()
            course.seance = self.seance.value()
            session.commit()
            self.reset()
            self.model.refresh()
            self.class_table.repaint()
        session.close()

    def sup_security(self):
        msg = QMessageBox()
        ret = msg.question(self, 'حذف', "متأكد من حذف هذا الصف ؟", msg.StandardButton.Yes | msg.StandardButton.No)

        if ret == msg.StandardButton.Yes:
            self.delete_class()
        else:
            self.reset()

    def delete_class(self):
        session = SessionLocal()

        course = session.query(Classes).filter(Classes.id == self.identifier).first()

        if course is not None:
            try:
                session.delete(course)
                session.commit()
            except IntegrityError:
                session.rollback()
                HelpLogic.error("هذا القسم موجود")
            finally:
                session.close()
                self.reset()
                self.set_table()

    def show_class(self):
        name = self.search.text()
        teacher = self.teacher_search.currentText()

        if name == "":
            name = None

        if teacher == "":
            teacher = None

        self.model.refresh(teacher, name) 

        self.class_table.repaint()
        self.nb.setText(str(self.model.rowCount()))       
 
    def reset(self):
        self.name.setText("")
        self.way.setCurrentIndex(-1)
        self.teacher.setCurrentIndex(-1)
        self.note.setText("")
        self.price.setText("")
        self.in_exchange.setCurrentIndex(-1)
        self.teacher_price.setValue(0)
        self.seance.setValue(0)


    def populate_combos(self):
        session = SessionLocal()
        teachers = session.query(Teachers).with_entities(Teachers.name).all()
        ways = session.query(Settings).with_entities(Settings.way_teaching).filter(Settings.way_teaching != None).all()
        session.close()

        for teacher in teachers:
            self.teacher.addItem(teacher[0])
            self.teacher_search.addItem(teacher[0])

        for way in ways:
            self.way.addItem(way[0])

        self.teacher.setCurrentIndex(-1)
        self.way.setCurrentIndex(-1)
        self.teacher_search.setCurrentIndex(-1)

    def printing_preview(self):
        try:

            title = "قائمة الأقسام"

            headers = ["الثمن", "الأستاذ", "الطريقة", "الإسم"]

            foot = f"""عدد الأقسام: {self.model.rowCount()}"""

            data = []

            for class_ in self.model.classes:
                row = [
                    str(class_.price),
                    class_.teacher,
                    class_.way,
                    class_.name
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
            headers = ["الثمن", "الأستاذ", "الطريقة", "الإسم"]
            data = []
            for class_ in self.model.classes:
                row = [
                    str(class_.price),
                    class_.teacher,
                    class_.way,
                    class_.name
                ]
                data.append(row)
            HelpLogic.excel(self, headers, data)
        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك تحميل الملف")

    # static methods
    @staticmethod
    def check(name):
        session = SessionLocal()
        data = session.query(Classes).filter(Classes.name == name).first()
        session.close()
        if data is None:
            return False
        else:
            return True

    @staticmethod    
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False


class ClasseleveLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "classeleve.ui"), self)

        self.model = None
        self.model_classeleve = None

        self.setup_students()
        self.setup_classeleve()
        self.populate_combo()

        self.setup()

    def setup(self):
        self.student_search_list.doubleClicked.connect(self.control)
        self.students.doubleClicked.connect(self.sup_security)
        self.student_search.textChanged.connect(self.show_students_list)
        self.search_btn.clicked.connect(self.show_classeleve)
        self.reset_btn.clicked.connect(self.reset)
        self.printing_btn.clicked.connect(self.printing_preview)
        self.export_btn.clicked.connect(self.excel)

        self.classes.setCurrentIndex(-1)

    def setup_classeleve(self):
        session = SessionLocal()

        self.model_classeleve = ClasseleveTableModel(session)

        self.students.setModel(self.model_classeleve)

        session.close()

    def setup_students(self):
        session = SessionLocal()

        self.model = StudentsSearchTableModel(session)

        self.student_search_list.setModel(self.model)

        session.close()

    def get_student_id(self):
        row = self.student_search_list.selectionModel().selectedRows()
        if not row:
            HelpLogic.error("يرجى تحديد التلميذ")
            return
        
        row_index = row[0].row()    

        identifier = self.model.data(self.model.index(row_index, 0), role=0)

        return identifier

    def control(self):
        class_name = self.classes.currentText()

        if class_name == "":
            HelpLogic.error("يرجى اختيار صف")
            return

        student_id = self.get_student_id()

        if self.check(student_id, class_name):
            HelpLogic.error("هذا التلميذ موجود في هذا الصف")
            return
        
        self.add(student_id, class_name)
    
    def add(self, student_id, class_name):
        session = SessionLocal()

        new_classeleve = ClassEleve(student_id=student_id, class_name=class_name)

        try:
            session.add(new_classeleve)
            session.commit()
        except IntegrityError as e:
            print(e)
            session.rollback()
            HelpLogic.error("هذا التلميذ موجود في هذا الصف")
        finally:
            session.close()
            self.setup_classeleve()
            self.model_classeleve.refresh(class_name=class_name)
            self.students.repaint()

    @staticmethod
    def check(student_id, class_name):        
        session = SessionLocal()
        data = session.query(ClassEleve).filter(ClassEleve.student_id == student_id, ClassEleve.class_name == class_name).first()
        session.close()
        if data is None:
            return False
        else:
            return True

    def sup_security(self):
        msg = QMessageBox()
        ret = msg.question(self, 'حذف', "متأكد من حذف هذا التلميذ ؟", msg.StandardButton.Yes | msg.StandardButton.No)

        if ret == msg.StandardButton.Yes:
            line = self.line_to_delete()
            self.delete(line)

    def line_to_delete(self):
        row = self.students.selectionModel().selectedRows()
        if not row:
            HelpLogic.error("يرجى تحديد التلميذ")
            return
        
        row_index = row[0].row()    

        identifier = self.model_classeleve.data(self.model_classeleve.index(row_index, 0), role=0)

        return identifier        

    def delete(self, line):
        session = SessionLocal()
        student = session.query(ClassEleve).filter(ClassEleve.id == line)
        if student.first() is not None:
            if student.first().class_name == "تأمين":
                HelpLogic.error("لا يمكن الحذف من هذه الفئة")
                session.close()
                return
            class_name = student.first().class_name
            try:
                student.delete()
                session.commit()
            except IntegrityError as e:
                print(e)
                session.rollback()
            finally:
                session.close()
                self.setup_classeleve()
                self.model_classeleve.refresh(class_name=class_name)
                self.students.repaint()
        else:
            HelpLogic.error("هذا التلميذ غير موجود")

    def show_classeleve(self):
        class_name = self.student_search.text()
        if class_name == "":
            class_name = None

        if self.classes.currentText() != "":
            class_name = self.classes.currentText()

        self.model_classeleve.refresh(class_name)
        self.students.repaint()

        self.nb.setText(str(self.model_classeleve.rowCount()))
        

    def show_students_list(self, student = None):
        if student == "":
            student = None

        self.model.refresh(student) 
        self.student_search_list.repaint()

    def reset(self):
        self.classes.setCurrentIndex(-1)

    def populate_combo(self):
        session = SessionLocal()
        classes = session.query(Classes).with_entities(Classes.name).all()
        session.close()

        for class_name in classes:
            self.classes.addItem(class_name[0])

        self.classes.setCurrentIndex(-1)

    def printing_preview(self):
        try:

            title = "قائمة التلاميذ"

            headers = ["رقم الهاتف", "تاريخ الولادة", "رقم الترسيم", "السيد(ة)"]

            foot = f"""عدد التلاميذ: {self.model_classeleve.rowCount()}"""

            intro = self.model_classeleve.intro + "\n"

            tracher = self.get_teacher_name(self.classes.currentText())

            intro += f"اسم المعلم: {tracher}"

            data = []

            for student in self.model_classeleve.classeseleve:
                row = [
                    str(student.num_tel),
                    student.birthday.strftime("%Y-%m-%d"),
                    str(student.num_inscrit),
                    student.name, 
                ]
                data.append(row)

            printer = Printing()
            printer.setup_document(data, headers, title, intro, foot)

            printer.exec()

        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك الطباعة")

    def excel(self):
        try:
            headers = ["رقم الهاتف", "تاريخ الولادة", "رقم الترسيم", "السيد(ة)"]
            data = []

            for student in self.model.students:
                row = [
                    str(student.num_tel),
                    student.birthday.strftime("%Y-%m-%d"),
                    str(student.num_inscrit),
                    student.name, 
                ]
                data.append(row)
            
            HelpLogic.excel(self, headers, data)

        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك تحميل الملف")

    def get_teacher_name(self, class_name):
        session = SessionLocal()
        teacher = session.query(Classes).filter(Classes.name == class_name).with_entities(Classes.teacher).first()
        session.close()
        return teacher


if __name__ == "__main__":
    app = QApplication([])
    window = ClassesLogic()
    window.show()
    app.exec()