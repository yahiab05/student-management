from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QDate
from .help import HelpLogic, Printing
from os import path
from .database import SessionLocal
from .models import Entery, Settings, OutMoney, Caisse, Bank
from tables_model.money_tables import EnteryTableModel, OutMoneyTableModel, BalanceTableModel, CaisseTabelModel, BankTabelModel
from sqlalchemy import func


class EnteryLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "entery.ui"), self)

        self.identifier = 0
        self.model = None

        self.cheq_num_on_off()
        self.populate_combo()
        self.reset()
        self.reset_filter()
        self.setup_table()
        self.setup_ui()

    def setup_ui(self):
        self.new_btn.clicked.connect(self.reset)
        self.add_btn.clicked.connect(lambda: self.control("add"))
        self.update_btn.clicked.connect(lambda: self.control("update"))
        self.reset_btn.clicked.connect(self.reset_filter)
        self.search_btn.clicked.connect(self.show_entery)
        self.way.currentTextChanged.connect(self.cheq_num_on_off)
        self.type.currentTextChanged.connect(self.get_code)
        self.code_input.valueChanged.connect(self.get_type)
        self.tbl.doubleClicked.connect(self.select)
        self.delete_btn.clicked.connect(self.sup_security) 
        self.bill_code.textChanged.connect(self.num_bill_control)
        self.printing_btn.clicked.connect(self.printing_preview)
        self.export_btn.clicked.connect(self.excel)

    def setup_table(self):
        session = SessionLocal()

        self.model = EnteryTableModel(session)

        self.tbl.setModel(self.model)

        self.total.setText(str(self.model.total_price)) 

        session.close()

    def control(self, action):
        name = self.name.text()
        date = self.date.date()
        types = self.type.currentText()
        way = self.way.currentText()
        price = self.price.text()
        note = self.note.text()
        code = self.code_input.value()
        num_bill = HelpLogic.next_bill_number()
        cheq_num = self.nb_cheque.text() if self.nb_cheque.text() != "" else 0

        going_to = self.bank_caisse.currentText()
        if going_to == "الخزينة":
            going_to = "caisse"
        else:
            going_to = "bank"

        if types == "" or code == 0:
            HelpLogic.error("نوع المدخول ضروري")
        elif way == "":
            HelpLogic.error("طريقة الدفع ضرورية")
        elif price == 0:
            HelpLogic.error("المبلغ ضروري")
        else:
            if action == "add":
                self.add(name, date, types, way, price, note, num_bill, cheq_num, code, going_to)
            else:
                self.update_entery(name, date, types, way, price, note, num_bill, cheq_num, code, going_to)
            self.reset()

    def add(self, name, date, types, way, price, note, num_bill, cheq_num, code, going_to):
        session = SessionLocal()

        try:
            income = Entery()

            income.name = name
            income.type = types
            income.way = way
            income.price = price
            income.note = note
            income.bill_number = num_bill
            income.cheq_num = cheq_num
            income.code = code
            income.addition_date = income.set_add_date(date)
            income.user = HelpLogic.get_username()

            session.add(income)
            session.commit()
            identifier = income.id
            HelpLogic.income_added(going_to, identifier, price, date, "من مداخيل")
        except Exception as e:
            print(e)
            session.rollback()
            HelpLogic.error("حدث خطأ")
        finally:
            session.close()
            self.setup_table()

    def select(self):
        row = self.tbl.selectionModel().selectedRows()
        if not row:
            HelpLogic.error("يرجى تحديد التلميذ")
            return
        
        row_index = row[0].row()    

        self.identifier = self.model.data(self.model.index(row_index, 0), role=0)
        types = self.model.data(self.model.index(row_index, 5), role=0)  

        self.tbl.clearSelection()

        if types == "تسجيل":
            self.identifier = 0
            HelpLogic.error("لا يمكن التحديث")
            return

        self.populate()

    def populate(self):
        session = SessionLocal()

        coming_from = HelpLogic.bank_or_caisse("i", self.identifier)

        try:
            income = session.query(Entery).filter(Entery.id == self.identifier).first()

            self.name.setText(income.name)
            self.date.setDate(income.get_add_date())
            self.type.setCurrentText(income.type)
            self.way.setCurrentText(income.way)
            self.price.setValue(income.price)
            self.note.setText(income.note)
            self.nb_cheque.setText(str(income.cheq_num))
            self.code_input.setValue(income.code)

            self.bank_caisse.setCurrentIndex(coming_from)
            self.bank_caisse.setEnabled(False)
        except Exception as e:
            print(e)
            session.rollback()
            HelpLogic.error("لا يمكن التحديث بعد الآن")
        finally:
            session.close()

    def update_entery(self, name, date, types, way, price, note, num_bill, cheq_num, code, going_to):
        session = SessionLocal()

        try:
            income = session.query(Entery).filter(Entery.id == self.identifier).first()

            income.name = name
            income.type = types
            income.way = way
            income.price = price
            income.note = note
            income.bill_number = num_bill
            income.cheq_num = cheq_num
            income.code = code
            income.addition_date = income.set_add_date(date)

            session.commit()
            HelpLogic.income_updated(going_to, self.identifier, price)
        except Exception as e:
            print(e)
            session.rollback()
            HelpLogic.error("لا يمكنك التحديث بعد الآن")
        finally:
            session.close()
            self.show_entery()
            self.reset()

    def sup_security(self):
        msg = QMessageBox()
        ret = msg.question(self, 'حذف', "متأكد من حذف هذا الدخل ؟", msg.StandardButton.Yes | msg.StandardButton.No)

        if ret == msg.StandardButton.Yes:
            self.delete_income()
        else:
            self.reset()

    def delete_income(self):
        session = SessionLocal()

        try:
            income = session.query(Entery).filter(Entery.id == self.identifier).first()

            session.delete(income)
            session.commit()
            caisse = session.query(Caisse).filter(Caisse.income_id == self.identifier).first()
            bank = session.query(Bank).filter(Bank.income_id == self.identifier).first()

            if caisse is not None:
                session.delete(caisse)
            elif bank is not None:
                session.delete(bank)

            session.commit()	
        except Exception as e:
            print(e)
            session.rollback()
            HelpLogic.error("لا يمكنك حذف هذا المصروف بعد الآن")
        finally:
            self.identifier = 0
            session.close()
            self.setup_table()
            self.reset()

    def reset(self):
        self.name.setText("")
        self.date.setDate(QDate.currentDate())
        self.code_input.setValue(0)
        self.price.setValue(0)
        self.type.setCurrentIndex(-1)
        self.way.setCurrentIndex(-1)
        self.note.setText("")
        self.nb_cheque.setText("")
        self.bank_caisse.setCurrentIndex(0)
        self.bank_caisse.setEnabled(True)

    def reset_filter(self):
        self.operatore.setCurrentIndex(-1)
        self.price_search.setValue(0)
        self.way_search.setCurrentIndex(-1)
        self.type_search.setCurrentIndex(-1)
        self.to.setDate(QDate.currentDate())
        self.du.setDate(QDate(2000, 1, 1))
        self.code.setValue(0)
        self.name_search.setText("")

    def show_entery(self):
        name = None if self.name_search.text() == "" else self.name_search.text()
        way = None if self.way_search.currentText() == "" else self.way_search.currentText()
        type = None if self.type_search.currentText() == "" else self.type_search.currentText()
        from_date = self.du.date().toPyDate()
        to_date = self.to.date().toPyDate()
        price = None if self.price_search.value() == 0 else self.price_search.value()
        operator = None if self.operatore.currentText() == "" else self.operatore.currentText()
        code = None if self.code.value() == 0 else self.code.value()

        self.model.refresh(operator,price, from_date, to_date, way, type, name, code)
        self.tbl.repaint()

        self.total.setText(str(self.model.total_price))

    def populate_combo(self):
        session = SessionLocal()

        ways = session.query(Settings).with_entities(Settings.way_payment).filter(Settings.way_payment != None).all()
        types = session.query(Settings).with_entities(Settings.entery).filter(Settings.entery != None).all()

        session.close()

        self.way.clear()
        self.type.clear()
        self.way_search.clear()
        self.type_search.clear()

        for type in types:
            self.type.addItem(type[0])
            self.type_search.addItem(type[0])

        for way in ways:
            self.way.addItem(way[0])
            self.way_search.addItem(way[0])

        self.way.setCurrentIndex(-1)
        self.type.setCurrentIndex(-1)
        self.way_search.setCurrentIndex(-1)
        self.type_search.setCurrentIndex(-1)

    def cheq_num_on_off(self):
        if self.way.currentText() == "صك":
            self.nb_cheque.setEnabled(True)
        else:
            self.nb_cheque.setEnabled(False)

    def get_code(self):
        session = SessionLocal()

        code = session.query(Settings).with_entities(Settings.entery_code).filter(Settings.entery == self.type.currentText()).first()

        if code is None:
            self.code_input.setValue(0)
        else:
            self.code_input.setValue(code[0])

        session.close()

    def get_type(self):
        session = SessionLocal()

        code = session.query(Settings).with_entities(Settings.entery).filter(Settings.entery_code == self.code_input.value()).first()

        if code is None:
            self.type.setCurrentIndex(-1)
        else:
            self.type.setCurrentText(code[0])

        session.close()

    def printing_preview(self):
        if self.bill_code.text() == "":
            try:

                title = "المداخيل"

                headers = ["المبلغ", "وسيلة الدخل", "الإسم", "نوع الدخل", "رقم الوصل", "التاريخ"]

                foot = f"""مجموع المداخيل: {self.model.total_price}"""

                data = []

                for ent in self.model.enteries:
                    row = [
                        str(ent.price),
                        ent.way,
                        ent.name,
                        ent.type, 
                        str(ent.bill_number), 
                        ent.addition_date.strftime("%Y-%m-%d")
                    ]
                    data.append(row)

                printer = Printing()
                printer.setup_document(data, headers, title, self.model.intro, foot)

                printer.exec()

            except Exception as e:
                print(e)
                HelpLogic.error("لا يمكنك الطباعة")

        else:
            code = self.bill_code.text()
            try:

                title = "وصل رقم: " + code

                headers = ["المبلغ", "وسيلة الدخل", "نوع الدخل", "التاريخ", "السيد(ة)"]

                session = SessionLocal()

                query = session.query(Entery).filter(Entery.bill_number == code).all()
                total = session.query(Entery).with_entities(func.sum(Entery.price)).filter(Entery.bill_number == code).first()

                session.close()

                total = str(total[0]) if total is not None else "0"

                foot = f" المجموع: {total}"

                data = []

                for ent in query:
                    row = [
                        str(ent.price),
                        ent.way,
                        ent.type, 
                        ent.addition_date.strftime("%Y-%m-%d"), 
                        ent.name
                    ]
                    data.append(row)

                printer = Printing()
                printer.setup_document(data, headers, title, "", foot)

                printer.exec()

            except Exception as e:
                print(e)
                HelpLogic.error("لا يمكنك الطباعة")

    def excel(self):
        if self.bill_code.text() == "":
            headers = ["المبلغ", "وسيلة الدخل", "الإسم", "نوع الدخل", "رقم الوصل", "التاريخ"] 
            data = []

            for ent in self.model.enteries:
                row = [
                    str(ent.price),
                    ent.way,
                    ent.name,
                    ent.type, 
                    str(ent.bill_number), 
                    ent.addition_date.strftime("%Y-%m-%d")
                ]
                data.append(row)

            HelpLogic.excel(self, headers, data)

        else:
            HelpLogic.error("لا يمكن القيام بهذه الميزة لفاتورة واحدة")

    def num_bill_control(self, c):
        try:
            code = self.bill_code.text()
            session = SessionLocal()

            data = session.query(Entery).with_entities(Entery.bill_number).filter(Entery.bill_number == code).order_by(Entery.bill_number.desc()).first()
            output = ''
            if data is not None:
                if int(code) > int(data[0]):
                    output = data[0]
                else:
                    output = code
            self.bill_code.setText(str(output))
        except ValueError:
            pass

class OutMoneyLogic(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "out.ui"), self)

        self.identifier = 0
        self.model = None

        self.reset()
        self.reset_filter()
        self.setup()
        self.populate_combo()
        self.setup_table()

    def setup(self):
        self.new_btn.clicked.connect(self.reset)
        self.add_btn.clicked.connect(lambda: self.control("add"))
        self.update_btn.clicked.connect(lambda: self.control("update"))
        self.delete_btn.clicked.connect(self.sup_security)
        self.tbl.doubleClicked.connect(self.select_out)
        self.search_btn.clicked.connect(self.show_out)
        self.reset_btn.clicked.connect(self.reset_filter)
        self.way.currentTextChanged.connect(self.cheq_num_on_off)
        self.type.currentTextChanged.connect(self.get_code)
        self.code_input.valueChanged.connect(self.get_type)
        self.printing_btn.clicked.connect(self.printing_preview)
        self.export_btn.clicked.connect(self.excel)

    def setup_table(self):
        session = SessionLocal()

        self.model = OutMoneyTableModel(session)

        self.tbl.setModel(self.model)

        self.total.setText(str(self.model.total_price))

        session.close()

    def control(self, action):
        name = self.name.currentText()
        bill_num = self.bill_num.text()
        date = self.date.date()
        types = self.type.currentText()
        way = self.way.currentText()
        cheq_num = self.nb_cheque.text()
        price = self.price.value()
        note = self.note.text()
        code = self.code_input.value()
        going_to = self.bank_caisse.currentText()
        if going_to == "الخزينة":
            going_to = "caisse"
        else:
            going_to = "bank"

        if name == "":
            HelpLogic.error("الإسم ضروري")
        elif types == "" or code == 0:
            HelpLogic.error("نوع المصروف ضروري")
        elif way == "":
            HelpLogic.error("طريقة الدفع ضرورية")
        elif price == 0:
            HelpLogic.error("المبلغ ضروري")
        else:
            if action == "add":
                if self.unique(bill_num, date.toPyDate()):
                    HelpLogic.error("هذا المصروف موجود")
                else:
                    self.add(name, date, types, way, price, note, bill_num, cheq_num, code, going_to)
            else:
                self.update_out(name, date, types, way, price, note, bill_num, cheq_num, code, going_to)
            self.reset()

    def add(self, name, date, types, way, price, note, num_bill, cheq_num, code, going_to):
        session = SessionLocal()

        try:
            if cheq_num == "":
                cheq_num = 0
            new_expense = OutMoney()

            new_expense.name = name
            new_expense.type = types
            new_expense.way = way
            new_expense.price = price
            new_expense.note = note
            new_expense.bill_num = num_bill
            new_expense.cheq_num = int(cheq_num)
            new_expense.code = code
            new_expense.date = new_expense.set_date(date)
            new_expense.user = HelpLogic.get_username()

            session.add(new_expense)
            session.commit()
            identifier = new_expense.id
            HelpLogic.expense_added(going_to, identifier, price, date, "من المصاريف")
        except Exception as e:
            print(e)
            session.rollback()
            HelpLogic.error("حدث خطاء")
        finally:
            session.close()
            self.reset()
            self.reset_filter()
            self.show_out()

    def update_out(self, name, date, types, way, price, note, num_bill, cheq_num, code, going_to):
        session = SessionLocal()

        try:
            expense = session.query(OutMoney).filter(OutMoney.id == self.identifier).first()

            expense.name = name
            expense.type = types
            expense.way = way
            expense.price = price
            expense.note = note
            expense.bill_num = num_bill
            expense.cheq_num = int(cheq_num)
            expense.date = expense.set_date(date)
            expense.code = code

            session.commit()
            HelpLogic.expense_updated(going_to, self.identifier, price)
        except Exception as e:
            print(e)
            session.rollback()
            HelpLogic.error("لا يمكنك التحديث بعد الآن")
        finally:
            session.close()
            self.show_out()
            self.reset()

    def sup_security(self):
        msg = QMessageBox()
        ret = msg.question(self, 'حذف', "متأكد من حذف هذا المصروف ؟", msg.StandardButton.Yes | msg.StandardButton.No)

        if ret == msg.StandardButton.Yes:
            self.delete_out()
        else:
            self.reset()

    def delete_out(self):
        session = SessionLocal()

        try:
            expense = session.query(OutMoney).filter(OutMoney.id == self.identifier).first()

            session.delete(expense)
            session.commit()
            caisse = session.query(Caisse).filter(Caisse.expense_id == self.identifier).first()
            bank = session.query(Bank).filter(Bank.expense_id == self.identifier).first()

            if caisse is not None:
                session.delete(caisse)
            elif bank is not None:
                session.delete(bank)

            session.commit()	
        except Exception as e:
            print(e)
            session.rollback()
            HelpLogic.error("لا يمكنك حذف هذا المصروف بعد الآن")
        finally:
            session.close()
            self.setup_table()
            self.reset()

    def reset(self):
        self.identifier = 0

        self.name.setCurrentIndex(-1)
        self.date.setDate(QDate.currentDate())
        self.type.setCurrentIndex(-1)
        self.way.setCurrentIndex(-1)
        self.price.setValue(0)
        self.note.setText("")
        self.bill_num.setText("")
        self.nb_cheque.setText("")
        self.code_input.setValue(0)

    def reset_filter(self):
        self.operatore.setCurrentIndex(-1)
        self.price_search.setValue(0)
        self.way_search.setCurrentIndex(-1)
        self.du.setDate(QDate(2000, 1, 1))
        self.to.setDate(QDate.currentDate())
        self.type_search.setCurrentIndex(-1)
        self.name_search.setCurrentIndex(-1)

    def show_out(self):
        name = None if self.name_search.currentText() == "" else self.name_search.currentText()
        way = None if self.way_search.currentText() == "" else self.way_search.currentText()
        type = None if self.type_search.currentText() == "" else self.type_search.currentText()
        from_date = self.du.date().toPyDate()
        to_date = self.to.date().toPyDate()
        price = None if self.price_search.value() == 0 else self.price_search.value()
        operator = None if self.operatore.currentText() == "" else self.operatore.currentText()
        code = None if self.code_input.value() == 0 else self.code_input.value()

        self.model.refresh(operator, price, from_date, to_date, way, type, name, code)
        self.tbl.repaint()

        self.total.setText(str(self.model.total_price))

    def populate_combo(self):
        session = SessionLocal()

        ways = session.query(Settings).with_entities(Settings.way_payment).filter(Settings.way_payment != None).all()
        types = session.query(Settings).with_entities(Settings.out_money).filter(Settings.out_money != None).all()
        names = session.query(Settings).with_entities(Settings.fr).filter(Settings.fr != None).all()

        self.name.clear()
        self.type.clear()
        self.way.clear()
        self.name_search.clear()
        self.type_search.clear()
        self.way_search.clear()

        for way in ways:
            self.way.addItem(way[0])
            self.way_search.addItem(way[0])

        for type in types:
            self.type.addItem(type[0])
            self.type_search.addItem(type[0])

        for name in names:
            self.name.addItem(name[0])
            self.name_search.addItem(name[0])

        self.way.setCurrentIndex(-1)
        self.type.setCurrentIndex(-1)
        self.way_search.setCurrentIndex(-1)
        self.type_search.setCurrentIndex(-1)
        self.name.setCurrentIndex(-1)
        self.name_search.setCurrentIndex(-1)

        session.close()

    def select_out(self):
        row = self.tbl.selectionModel().selectedRows()
        if not row:
            HelpLogic.error("يرجى تحديد المصروف")
            return
        
        row_index = row[0].row()    

        self.identifier = self.model.data(self.model.index(row_index, 0), role=0)

        self.tbl.clearSelection()
        self.populate()

    def populate(self):
        session = SessionLocal()

        out = session.query(OutMoney).filter(OutMoney.id == self.identifier).first()

        if out is not None:
            self.name.setCurrentText(out.name)
            self.date.setDate(out.get_date())
            self.type.setCurrentText(out.type)
            self.way.setCurrentText(out.way)
            self.price.setValue(out.price)
            self.note.setText(out.note)
            self.bill_num.setText(str(out.bill_num))
            self.nb_cheque.setText(str(out.cheq_num))
            self.code_input.setValue(out.code)
            self.bank_caisse.setCurrentIndex(HelpLogic.bank_or_caisse("e", self.identifier))

        session.close()

    @staticmethod
    def unique(bill_num, date):
        session = SessionLocal()

        out = session.query(OutMoney).filter(OutMoney.bill_num == bill_num, OutMoney.date == date).first()

        session.close()

        if out:
            return True

        return False
    
    def cheq_num_on_off(self):
        if self.way.currentText() == "صك":
            self.nb_cheque.setEnabled(True)
        else:    
            self.nb_cheque.setEnabled(False)

    def get_code(self):
        session = SessionLocal()

        code = session.query(Settings).with_entities(Settings.out_code).filter(Settings.out_money == self.type.currentText()).first()

        if code is None:
            self.code_input.setValue(0)
        else:
            self.code_input.setValue(code[0])

        session.close()

    def get_type(self):
        session = SessionLocal()

        code = session.query(Settings).with_entities(Settings.out_money).filter(Settings.out_code == self.code_input.value()).first()

        if code is None:
            self.type.setCurrentIndex(-1)
        else:
            self.type.setCurrentText(code[0])

        session.close()

    def printing_preview(self):
        try:

            title = "المصاريف"

            headers = ["المبلغ", "وسيلة الدفع", "نوع المصروف", "التاريخ", "الرمز"]

            foot = f"""مجموع المصاريف: {self.model.total_price}"""

            data = []

            for out in self.model.outs:
                row = [
                    str(out.price),
                    out.way,
                    out.type,
                    out.date.strftime("%Y-%m-%d"), 
                    str(out.code)
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
            headers = ["المبلغ", "وسيلة الدفع", "نوع المصروف", "التاريخ", "الرمز"]
            data = []

            for out in self.model.outs:
                row = [
                    str(out.price),
                    out.way,
                    out.type,
                    out.date.strftime("%Y-%m-%d"), 
                    str(out.code)
                ]
                data.append(row)
        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك تحميل الملف")

class BalanceLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "solde.ui"), self)

        self.model = None

        self.setup_table()
        self.reset()
        self.populate_combo()
        self.setup()

    def setup(self):
        self.search_btn.clicked.connect(self.show_table)
        self.reset_btn.clicked.connect(self.reset)
        self.printing_btn.clicked.connect(self.printing_preview)
        self.export_btn.clicked.connect(self.excel)

    def setup_table(self):
        session = SessionLocal()

        self.model = BalanceTableModel(session)

        self.tbl.setModel(self.model)

        self.total_out.setText(str(self.model.total_expenses))
        self.total_in.setText(str(self.model.total_income))
        self.solde.setText(str(self.model.balance))

        session.close()

    def populate_combo(self):
        session = SessionLocal()

        ways = session.query(Settings).with_entities(Settings.way_payment).filter(Settings.way_payment != None).all()

        self.way.clear()

        for way in ways:
            self.way.addItem(way[0])

        session.close()

        self.way.setCurrentIndex(-1)

    def show_table(self):
        op = None if self.operatore.currentText() == "" else self.operatore.currentText()
        price = None if self.price_input.value() == 0 else self.price_input.value()
        from_date = self.du.date().toPyDate()
        to_date = self.to.date().toPyDate()
        way = None if self.way.currentText() == "" else self.way.currentText() 

        self.model.refresh(op, price, from_date, to_date, way)
        self.tbl.repaint()

        self.total_out.setText(str(self.model.total_expenses))
        self.total_in.setText(str(self.model.total_income))
        self.solde.setText(str(self.model.balance))


    def reset(self):
        self.operatore.setCurrentIndex(-1)
        self.price_input.setValue(0)
        self.du.setDate(QDate(2000, 1, 1))
        self.to.setDate(QDate.currentDate())
        self.way.setCurrentIndex(-1)

    def printing_preview(self):
        try:

            title = "الحاصل"

            headers = ["المبلغ المقبول" ,"المبلغ المصروف", "وسيلة الدخل/المصروف", "التاريخ", "الاسم"]

            foot = f"""مجموع المداخيل: {self.model.total_income} \n 
            مجموع المصاريف: {self.model.total_expenses} \n
            الحاصل: {self.model.balance}"""

            data = []

            for s in self.model.balances:
                row = [
                    str(s.income),
                    str(s.expenses),
                    s.way,
                    s.date.strftime("%Y-%m-%d"), 
                    s.name
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
            headers = ["المبلغ المقبول" ,"المبلغ المصروف", "وسيلة الدخل/المصروف", "التاريخ", "الاسم"]

            data = []

            for s in self.model.balances:
                row = [
                    str(s.income),
                    str(s.expenses),
                    s.way,
                    s.date.strftime("%Y-%m-%d"), 
                    s.name
                ]
                data.append(row)

            HelpLogic.excel(self, headers, data)
        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك تحميل الملف")

class BankLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "bank.ui"), self)

        self.model = None

        self.setup_table()  
        self.reset()
        self.setup()

    def setup(self):
        self.search_btn.clicked.connect(self.show_table)
        self.reset_btn.clicked.connect(self.reset)
        self.printing_btn.clicked.connect(self.printing_preview)
        self.export_btn.clicked.connect(self.excel)

    def setup_table(self):
        session = SessionLocal()    

        self.model = BankTabelModel(session)

        self.tbl.setModel(self.model)

        self.total_out.setText(str(self.model.total_expenses))
        self.total_in.setText(str(self.model.total_income))
        self.solde.setText(str(self.model.balance))

        session.close()

    def show_table(self):
        op = None if self.operatore.currentText() == "" else self.operatore.currentText()
        price = None if self.price_search.value() == 0 else self.price_search.value()
        from_date = self.du.date().toPyDate()
        to_date = self.to.date().toPyDate()

        self.model.refresh(op, price, from_date, to_date)
        self.tbl.repaint()

        self.total_out.setText(str(self.model.total_expenses))
        self.total_in.setText(str(self.model.total_income))
        self.solde.setText(str(self.model.balance))

    def reset(self):
        self.operatore.setCurrentIndex(-1)
        self.price_search.setValue(0)
        self.du.setDate(QDate(2000, 1, 1))
        self.to.setDate(QDate.currentDate())

    def printing_preview(self):
        try:

            title = "البنك"

            headers = ["المبلغ المقبول", "المبلغ المصروف", "التاريخ"]

            foot = f"""مجموع المداخيل: {self.model.total_income} \n 
            مجموع المصاريف: {self.model.total_expenses} \n
            الحاصل: {self.model.balance}"""

            data = []

            for b in self.model.banks:
                row = [
                    str(b.income),
                    str(b.expense),    
                    b.date.strftime("%Y-%m-%d")
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
            headers = ["المبلغ المقبول", "المبلغ المصروف", "التاريخ"]
            data = []

            for b in self.model.banks:
                row = [
                    str(b.income),
                    str(b.expense),    
                    b.date.strftime("%Y-%m-%d")
                ]
                data.append(row)

            HelpLogic.excel(self, headers, data)
        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك تحميل الملف")

class CaisseLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "caisse.ui"), self)

        self.model = None

        self.date.setDate(QDate.currentDate())

        self.setup_table()
        self.reset()
        self.setup()

    def setup(self):
        self.search_btn.clicked.connect(self.show_table)
        self.reset_btn.clicked.connect(self.reset)
        self.to_caisse_btn.clicked.connect(lambda: self.control("bank", "caisse"))
        self.to_bank_btn.clicked.connect(lambda: self.control("caisse", "bank"))
        self.printing_btn.clicked.connect(self.printing_preview)
        self.export_btn.clicked.connect(self.excel)

    def setup_table(self):
        session = SessionLocal()

        self.model = CaisseTabelModel(session)

        self.tbl.setModel(self.model)

        self.total_out.setText(str(self.model.total_expenses))
        self.total_in.setText(str(self.model.total_income))
        self.solde.setText(str(self.model.balance))

        session.close()

    def show_table(self):
        op = None if self.operatore.currentText() == "" else self.operatore.currentText()
        price = None if self.price_search.value() == 0 else self.price_search.value()
        from_date = self.du.date().toPyDate()
        to_date = self.to.date().toPyDate()

        self.model.refresh(op, price, from_date, to_date)
        self.tbl.repaint()

        self.total_out.setText(str(self.model.total_expenses))
        self.total_in.setText(str(self.model.total_income))
        self.solde.setText(str(self.model.balance))

    def reset(self):
        self.operatore.setCurrentIndex(-1)
        self.price_search.setValue(0)
        self.du.setDate(QDate(2000, 1, 1))
        self.to.setDate(QDate.currentDate())

    def control(self, from_acc, to_acc):
        if self.price.value() == 0:
            HelpLogic.error("يجب ادخال المبلغ")
            return
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setText("هل تريد التحويل")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        msg = msg.exec()

        if msg == QMessageBox.StandardButton.Yes:
            self.transfer_funds(from_acc, to_acc)

    def transfer_funds(self, from_account, to_account):
        amount = self.price.value()
        note = self.note.text()
        date = self.date.date()

        session = SessionLocal()
        c = Caisse()
        b = Bank()

        if from_account == "caisse" and to_account == "bank":
            c.expense = amount
            c.note = note
            c.date = c.set_date(date)

            b.income = amount
            b.note = note
            b.date = b.set_date(date)

        elif from_account == "bank" and to_account == "caisse":
            b.expense = amount
            b.note = note
            b.date = b.set_date(date)

            c.income = amount
            c.note = note
            c.date = c.set_date(date)
        else:
            HelpLogic.error("خطاء في التحويل")

        try:
            session.add(c)
            session.add(b)
            session.commit()
            HelpLogic.error("تم التحويل بنجاح")
        except Exception as e:
            print(e)
            session.rollback()
            HelpLogic.error("خطاء في التحويل")
        finally:
            session.close()
            self.setup_table()
            self.date.setDate(QDate.currentDate())
            self.price.setValue(0)
            self.note.setText("")

    def printing_preview(self):
        try:

            title = "الخزينة"

            headers = ["المبلغ المقبول", "المبلغ المصروف", "التاريخ"]

            foot = f"""مجموع المداخيل: {self.model.total_income} \n 
            مجموع المصاريف: {self.model.total_expenses} \n
            الحاصل: {self.model.balance}"""

            data = []

            for b in self.model.caisse:
                row = [
                    str(b.income),
                    str(b.expense),    
                    b.date.strftime("%Y-%m-%d")
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
            headers = ["المبلغ المقبول", "المبلغ المصروف", "التاريخ"]

            data = []

            for b in self.model.caisse:
                row = [
                    str(b.income),
                    str(b.expense),    
                    b.date.strftime("%Y-%m-%d")
                ]
                data.append(row)

            HelpLogic.excel(self, headers, data)
        except Exception as e:
            print(e)
            HelpLogic.error("لا يمكنك تحميل الملف")