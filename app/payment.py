from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import QDate
from .models import Entery, Settings, ClassEleve, Users, Classes, Students, Caisse
from .database import SessionLocal
from tables_model.students_model import StudentsSearchTableModel
from tables_model.payment_model import PaymentTableModel
from .help import HelpLogic, Printing
from os import path
from sqlalchemy import extract

class AddPayment(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "add_payment.ui"), self)

        self.model = None
        self.identifier = 0
        self.momentane = []

        self.date.setDate(QDate.currentDate())

        self.setup_student_search()
        self.cheq_num_on_off()
        self.populate_combo()
        self.setup()
        self.show_bill()

    def setup(self):
        self.add_btn.clicked.connect(self.control)
        self.reset_btn.clicked.connect(self.reset)
        self.confirm_btn.clicked.connect(self.confirm_bill)
        self.bill_tbl.doubleClicked.connect(self.delete_from_bill)
        self.student_list.doubleClicked.connect(self.select_student)
        self.search_student.textChanged.connect(self.search_student_func)
        self.way.currentTextChanged.connect(self.cheq_num_on_off)
        self.classroom.currentTextChanged.connect(lambda: self.set_price(self.classroom.currentText()))

    def setup_student_search(self):
        session = SessionLocal()

        self.model = StudentsSearchTableModel(session)

        self.student_list.setModel(self.model)

        session.close()

    def search_student_func(self, name = None):
        name = None if name == "" else name

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
        self.populate_classes(self.identifier)
        self.note_payment()

    def note_payment(self):
        session = SessionLocal()

        note = session.query(Students).filter(Students.num_inscrit == self.identifier).first().note

        if note: 
            HelpLogic.error(note)

        session.close()

    def control(self):
        name = self.name.text()
        classroom = self.classroom.currentText()
        price = self.price.text()
        date = self.date.date()
        way = self.way.currentText()
        cheq_num = self.cheq_num.text()

        if len(name) == 0:
            HelpLogic.error("ينقص الإسم")
        elif len(classroom) == 0:
            HelpLogic.error("الوسيلة ضرورية")
        elif len(way) == 0:
            HelpLogic.error("وسيلة الدفع ضرورية")
        elif way == 'صك' and len(cheq_num) == 0:
            HelpLogic.error("رقم الصك ضروري")
        elif self.price.value() == 0:
            HelpLogic.error("خطأ في الثمن")
        elif self.is_unique(self.identifier, classroom, date):
            HelpLogic.error("لقد تم إصدار هذا الوصل")
        else:
            self.add(name, classroom, price, way, cheq_num, date)

    def add(self, name, classroom, price, way, cheq_num, date):
        payment = {
            "num_inscrit": self.identifier,
            "bill_number": 0,
            "name": name,
            "classroom": classroom,
            "price": price,
            "way": way,
            "cheq_num": cheq_num if cheq_num != "" else 0,
            "addition_date": QDate.currentDate().toPyDate(),
            "payment_date": date.toPyDate(),
            "type" : "تسجيل", 
            "code" : 13, 
            "note" : "", 
            "user" : "Yahia"
            }
    
        self.momentane.append(payment)

        self.show_bill()

    def delete_from_bill(self, row):
        self.momentane.pop(row.row())

        self.show_bill()

    def show_bill(self):
        self.bill_tbl.setRowCount(len(self.momentane))

        for i in range(len(self.momentane)):
            row = self.momentane[i]
            self.bill_tbl.setItem(i, 0, QTableWidgetItem(str(row["num_inscrit"])))
            self.bill_tbl.setItem(i, 1, QTableWidgetItem(str(row["name"])))
            self.bill_tbl.setItem(i, 2, QTableWidgetItem(str(row["classroom"])))
            self.bill_tbl.setItem(i, 3, QTableWidgetItem(str(row["price"])))
            self.bill_tbl.setItem(i, 4, QTableWidgetItem(str(row["payment_date"].strftime("%Y-%m"))))
            self.bill_tbl.setItem(i, 5, QTableWidgetItem(str(row["way"])))
            self.bill_tbl.setItem(i, 6, QTableWidgetItem(str(row["cheq_num"])))

    def confirm_bill_security(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText("هل تريد تاكيد الفاتورة؟")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            self.confirm_bill()

    def confirm_bill(self):
        bill_number = HelpLogic.next_bill_number()

        for i in self.momentane:
            i["bill_number"] = bill_number
        
        session = SessionLocal()

        try:
            payments = [Entery(**ent) for ent in self.momentane]
            session.add_all(payments)
            session.flush()

            caisses = []

            for i in range(len(self.momentane)):
                row = Caisse(income_id= payments[i].id, income = payments[i].price, note = "تسجيل",
                date = QDate.currentDate().toPyDate())
                caisses.append(row)

            session.add_all(caisses)
            session.commit()

            self.momentane = []
            self.caisse_momentane = []
            self.caisse_id_difference = 1
            HelpLogic.error("تم التاكيد")

        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()
            self.momentane = []
            self.caisse_momentane = []
            self.caisse_id_difference = 0
            self.reset()
            self.show_bill()


    def populate_combo(self):
        session = SessionLocal()

        ways = session.query(Settings).with_entities(Settings.way_payment).filter(
            Settings.way_payment != None).all()
        
        self.way.clear()

        for way in ways:
            self.way.addItem(way[0])

        session.close()

        self.way.setCurrentIndex(-1)

    def populate_classes(self, identifier): 
        session = SessionLocal()

        classes = session.query(ClassEleve).with_entities(ClassEleve.class_name).filter(
            ClassEleve.student_id == identifier).all()
        
        self.classroom.clear()

        for class_name in classes:
            self.classroom.addItem(class_name[0])

        session.close()

        self.classroom.setCurrentIndex(-1)    
    
    def reset(self):
        self.name.setText("")
        self.classroom.setCurrentIndex(-1)
        self.way.setCurrentIndex(-1)
        self.price.setValue(0)
        self.cheq_num.setText("")
        self.date.setDate(QDate.currentDate())
        self.identifier = 0

    def set_price(self, classroom):
        if classroom != "":
            session = SessionLocal()

            price = session.query(Classes).with_entities(Classes.price).filter(
                Classes.name == self.classroom.currentText()).first()
            
            self.price.setValue(price[0])

            session.close()


    def is_unique(self, identifier, classroom, date):
        session = SessionLocal()

        # Checking for payment with the same identifier, classroom, and matching year and month
        if classroom == "تأمين":
            payment = session.query(Entery).filter(
                Entery.num_inscrit == identifier,
                Entery.classroom == classroom,
                extract('year', Entery.payment_date) == date.year()
            ).first()
            
            # If payment exists and classroom is "تأمين", check if the year is different
            if payment:
                session.close()
                return True  # "تأمين" payment is considered unique based on different year
        else:
            payment = session.query(Entery).filter(
                Entery.num_inscrit == identifier,
                Entery.classroom == classroom,
                extract('year', Entery.payment_date) == date.year(),
                extract('month', Entery.payment_date) == date.month()
            ).first()

            # If payment exists and classroom is not "تأمين", it's not unique if same year and month
            if payment:
                session.close()
                return True  # It's not unique if same identifier, classroom, year, and month

        # Check in momentane for non-database temporary data
        if len(self.momentane) > 0:
            for i in self.momentane:
                if i["classroom"] == "تأمين" and classroom == "تأمين":
                    if i['payment_date'].year == date.year():
                        return True
                else:
                    print(i["num_inscrit"], identifier, i["classroom"], classroom, i["payment_date"].year, date.year(), i["payment_date"].month, date.month())
                    if i["num_inscrit"] == identifier and i["classroom"] == classroom and i["payment_date"].year == date.year() and i["payment_date"].month == date.month():
                        return True

        session.close()
        return False  # If no match, it's unique
    def cheq_num_on_off(self):
        if self.way.currentText() == "صك":
            self.cheq_num.setEnabled(True)
        else:
            self.cheq_num.setEnabled(False)

class ViewPayment(QWidget):
    def __init__(self):
        super().__init__()

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "view_payment.ui"), self)

        self.to.setDate(QDate.currentDate())
        self.du.setDate(QDate(2000, 1, 1))

        self.identifier = 0

        self.setup_table()
        self.setup()

    def setup(self):
        self.search_ent.textChanged.connect(lambda: self.show_students_list(self.search_ent.text()))
        self.student_list.itemDoubleClicked.connect(self.select_student)
        self.search_btn.clicked.connect(self.search)
        self.reset_btn.clicked.connect(self.reset)
        self.reg_tbl.clicked.connect(self.select_row)
        self.update_btn.clicked.connect(self.edit_price) 
        self.cancel_btn.clicked.connect(self.cancel)
        self.printing_btn.clicked.connect(self.printing_preview)
        self.export_btn.clicked.connect(self.excel)

    def setup_table(self):
        session = SessionLocal()

        self.model = PaymentTableModel(session)

        self.reg_tbl.setModel(self.model)

        self.total.setText(str(self.model.total_price))
        self.nb.setText(str(self.model.rowCount()))

        session.close()

    def search(self):
        student = self.search_ent.text() if self.search_ent.text() != "" else None
        from_date = self.du.date().toPyDate()
        to_date = self.to.date().toPyDate()
        classroom = self.classroom.currentText() if self.classroom.currentText() != "" else None
        num_inscrit = self.num_inscrit.text() if self.num_inscrit.text() != "" else None
        way = self.way.currentText() if self.way.currentText() != "" else None

        print(from_date, to_date)

        self.model.refresh(classroom, from_date, to_date, way, num_inscrit, student)
        self.reg_tbl.repaint()

        self.total.setText(str(self.model.total_price))
        self.nb.setText(str(self.model.rowCount()))

    def select_student(self):
        name = self.student_list.currentItem().text()

        self.search_ent.setText(name)

    def show_students_list(self, student = ""):
        session = SessionLocal()
        if student:
            query = session.query(Entery).with_entities(Entery.name).filter(Entery.name.contains(student), 
                                                      Entery.classroom != None)
        else:
            query = session.query(Entery).with_entities(Entery.name).filter(Entery.classroom != None)

        result = query.distinct().all()

        self.student_list.clear()
        for name in result:
            self.student_list.addItem(name[0])

        session.close()

    def reset(self):
        self.search_ent.setText("")
        self.du.setDate(QDate(2000, 1, 1))
        self.to.setDate(QDate.currentDate())
        self.classroom.setCurrentIndex(-1)
        self.way.setCurrentIndex(-1)
        self.num_inscrit.setText("")

        self.show_students_list()

    def select_row(self):
        if self.has_access():
            row = self.reg_tbl.selectionModel().selectedRows()
            if not row:
                HelpLogic.error("يرجى تحديد وصل:")
                return
            
            row_index = row[0].row()
            
            self.identifier = self.model.data(self.model.index(row_index, 0), role=0)

            self.reg_tbl.clearSelection()
            self.stackedWidget.setCurrentIndex(1)
            self.search_frame.setEnabled(False)
            self.set_old_price(self.identifier)
        else:
            HelpLogic.error("ليس لديك صلاحية")

    def set_old_price(self, identifier):
        session = SessionLocal()

        payment = session.query(Entery).filter(Entery.id == identifier).first()

        session.close()

        self.previous_price.setText(str(payment.price))  

    def has_access(self):
        username = HelpLogic.get_username()
        session = SessionLocal()

        user = session.query(Users).filter(Users.username == username).first()

        if user.role.payment_editting:
            session.close()

            return True
        session.close()

        return False

    def edit_price(self):
        if self.new_price.value() > 0:
            try:
                session = SessionLocal()

                payment = session.query(Entery).filter(Entery.id == self.identifier).first()

                payment.price = self.new_price.value()


                HelpLogic.income_updated("caisse", self.identifier, self.new_price.value())

                session.commit()

            except Exception as e:
                print(e)
                session.rollback()
                HelpLogic.error("لا يمكنك التحديث بعد الآن")
            finally:
                session.close()
                self.cancel()
                self.identifier = 0
                self.setup_table()
        else:
            HelpLogic.error("السعر يجب ان يكون اكبر من صفر")

    def cancel(self):
        self.stackedWidget.setCurrentIndex(0)
        self.new_price.setValue(0)
        self.previous_price.setText("")
        self.search_frame.setEnabled(True)

    def populate_combos(self):
        session = SessionLocal()

        classes = session.query(Entery).with_entities(Entery.classroom).filter(
            Entery.classroom != None).distinct().all()
        
        ways = session.query(Entery).with_entities(Entery.way).filter(
            Entery.way != None).distinct().all()
        
        self.classroom.clear()
        self.way.clear()
        
        for class_name in classes:
            self.classroom.addItem(class_name[0])

        for way in ways:
            self.way.addItem(way[0])

        session.close()

        self.classroom.setCurrentIndex(-1)
        self.way.setCurrentIndex(-1)

    def printing_preview(self):
        try:

            title = "قائمة الوصولات"

            headers = ["طريقة الخلاص", "المبلغ", "مقابل شهر", "بعنوان", "رقم الوصل", "السيد(ة)"]

            foot = f" المجموع: {self.model.total_price}"

            data = []

            for payment in self.model.payments:
                row = [
                    str(payment.way),
                    payment.price,
                    payment.payment_date.strftime("%Y-%m"),
                    payment.classroom,
                    str(payment.bill_number),
                    payment.name
                ]
                data.append(row)

            printer = Printing()
            printer.setup_document(data, headers, title, '', foot)

            printer.exec()

        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك الطباعة")

    def excel(self):
        try:
            headers = ["طريقة الخلاص", "المبلغ", "مقابل شهر", "بعنوان", "رقم الوصل", "السيد(ة)"]
            data = []

            for payment in self.model.payments:
                row = [
                    str(payment.way),
                    payment.price,
                    payment.payment_date.strftime("%Y-%m"),
                    payment.classroom,
                    str(payment.bill_number),
                    payment.name
                ]
                data.append(row)

            HelpLogic.excel(self, headers, data)
        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك تحميل الملف")

class ViewNotPayedLogic(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "view_not_payed.ui"), self)

        self.year.setValue(QDate.currentDate().year())

        self.setup()

    def setup(self):
        self.search_btn.clicked.connect(self.search)
        self.reset_btn.clicked.connect(self.reset)

    def search(self):
        class_ = self.classroom.currentText()
        session = SessionLocal()
        if not class_:
            HelpLogic.error("يرجى تحديد الصف")
            return

        elif class_ == "تأمين":
            year = self.year.value()

            query = session.query(Entery).with_entities(Entery.num_inscrit).filter(Entery.classroom == class_, 
                                                                        extract("year", Entery.payment_date) == year).all()

            query = [student[0] for student in query]

            students = session.query(Students).filter(Students.num_inscrit.not_in(query)).all()

            self.tbl.clear()

            for s in students:
                self.tbl.addItem(s.name)

        else:
            month = self.month.value()
            year = self.year.value()

            query = session.query(Entery).with_entities(Entery.num_inscrit).filter(Entery.classroom == class_, 
                                extract("month", Entery.payment_date) == month, 
            extract("year", Entery.payment_date) == year).all()

            query = [student[0] for student in query]

            students = session.query(Students).filter(Students.num_inscrit.not_in(query)).all()

            self.tbl.clear()

            for s in students:
                self.tbl.addItem(s.name)

        session.close()

    def reset(self):
        self.classroom.setCurrentIndex(-1)
        self.month.setValue(1)
        self.year.setValue(QDate.currentDate().year())

    def populate_classes(self):
        session = SessionLocal()

        classes = session.query(ClassEleve).with_entities(ClassEleve.class_name).distinct().all()
        
        self.classroom.clear()

        for class_name in classes:
            self.classroom.addItem(class_name[0])

        session.close()

        self.classroom.setCurrentIndex(-1)