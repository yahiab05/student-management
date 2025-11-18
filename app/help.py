from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtWidgets import QMessageBox, QDialog, QApplication, QFileDialog
from .database import SessionLocal
from .models import Entery, Caisse, Bank
from PyQt6.uic import loadUi
from os import path
from sqlalchemy import text
from jinja2 import Template
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
import xlsxwriter.exceptions
from xlsxwriter import Workbook


class HelpLogic:
    @staticmethod
    def set_username(username: str) -> None:
        settings = QSettings("Dar Coran", "Gestion")
        settings.setValue("username", username)

    @staticmethod
    def get_username() -> str:
        settings = QSettings("Dar Coran", "Gestion")
        return settings.value("username", "") if settings.value("username") is not None and not "" else "yahia"
    
    @staticmethod
    def error(message: str) -> None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(message)
        msg.exec()
        msg.show()

    @staticmethod
    def next_bill_number() -> int:
        session = SessionLocal()

        bill = session.query(Entery).order_by(Entery.bill_number.desc()).first()

        if bill is None:
            return 1
        else:
            return bill.bill_number + 1
        
    @staticmethod
    def income_added(where, id, amount , date, note) -> None:
        session = SessionLocal()

        if where == "bank":
            bank = Bank(income_id=id,income=amount, note=note)
            bank.date = bank.set_date(date)
            session.add(bank)
        else:
            caisse = Caisse(income_id=id, income=amount, note=note)
            caisse.date = caisse.set_date(date)
            session.add(caisse)

        session.commit()
        session.close()

    @staticmethod
    def expense_added(where, id, amount, date, note) -> None:
        session = SessionLocal()

        if where == "bank":
            bank = Bank(expense_id=id, expense=amount, note=note)
            bank.date = bank.set_date(date)
            session.add(bank)
        else:
            caisse = Caisse(expense_id=id, expense=amount, note=note)
            caisse.date = caisse.set_date(date) 
            session.add(caisse)

        session.commit()
        session.close()

    @staticmethod
    def income_updated(where, id, amount):
        session = SessionLocal()

        if where == "bank":
            bank = session.query(Bank).filter(Bank.income_id == id).first()            
            bank.income = amount
        else:
            caisse = session.query(Caisse).filter(Caisse.income_id == id).first()            
            caisse.income = amount

        session.commit()
        session.close()

    @staticmethod
    def expense_updated(where, id, amount) -> None:
        session = SessionLocal()

        if where == "bank":
            bank = session.query(Bank).filter(Bank.expense_id == id).first()            
            bank.expense = amount
        else:
            caisse = session.query(Caisse).filter(Caisse.expense_id == id).first()            
            caisse.expense = amount

        session.commit()
        session.close()

    @staticmethod
    def get_next_auto_increment():
        session = SessionLocal()
        
        query = text(f"""
            SELECT AUTO_INCREMENT 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = :db_name AND TABLE_NAME = :table_name
        """)
        
        result = session.execute(query, {"db_name": "students1", "table_name": "entery"}).scalar()
        
        session.close()
        return result
        
    @staticmethod
    def bank_or_caisse(where, identifier) -> int:
        session = SessionLocal()

        if where == "i":
            caisse = session.query(Caisse).filter(Caisse.income_id == identifier).first()

            if caisse is not None:
                return 0
            else:
                return 1
        else:
            caisse = session.query(Caisse).filter(Caisse.expense_id == identifier).first()

            if caisse is not None:
                return 0
            else:
                return 1
            
    @staticmethod
    def excel(self, headers, data):
        file = QFileDialog.getSaveFileName(self, 'Save file', '', '*.xlsx')
        try:
            book = Workbook(file[0])
            sheet = book.add_worksheet("dataimported")

            # initialize rows and columns of the worksheet
            row = 0
            col = 0

            # Insert the columns name in to the excel
            for heading in headers:
                sheet.write(row, col, heading)
                col += 1
            # Create a For loop to iterate through each entries in the db file
            for entry in data:
                row += 1
                col = 0
                for data_val in entry:
                    sheet.write(row, col, data_val)
                    col += 1

            book.close()
        except xlsxwriter.exceptions.FileCreateError:
            pass


class Printing(QDialog):
    def __init__(self):
        super().__init__()

        ui_path = path.abspath("../dar coran(new)/ui/printing.ui")  # Convert to absolute path
        loadUi(ui_path, self)

        self.adapt_size()

        self.setup()

    def setup(self):
        self.printing.clicked.connect(self.print_file)
        self.cancel.clicked.connect(self.canceled)

    def adapt_size(self):
        """Resizes the QDialog based on screen height."""
        screen = QApplication.primaryScreen().geometry()  # Get screen size
        screen_height = screen.height()  # Get screen height
        self.setMinimumHeight(int(screen_height * 0.6))  # Set height to 60% of screen
        self.setMaximumHeight(int(screen_height * 0.9))  # Max height is 90% of screen

    def setup_document(self, data, headers, title="", intro="", foot=""):
        self.printing_plain.clear()
        self.printing_plain.setFontPointSize(20)
        self.printing_plain.append(title)
        self.printing_plain.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.printing_plain.append("""   """)
        self.printing_plain.setFontPointSize(12)
        self.printing_plain.append(intro)
        self.printing_plain.append("""   """)
        table = """
                        <style>
                        table {
                            font-family: arial, sans-serif;
                            border-collapse: collapse;
                            width: 100%;
                        }

                        td, th {
                            border: 1px solid #dddddd;
                            text-align: center;
                            padding: 4px;
                        }
                        </style>

                        <table border="1" width="100%">
                            <tr>{% for header in headers %}<th>{{header}}</th>{% endfor %}</tr>
                            {% for row in rows %}<tr>
                                {% for element in row %}<td>
                                    {{element}}
                                </td>{% endfor %}
                            </tr>{% endfor %}
                        </table>
                        """
        self.printing_plain.append(Template(table).render(headers=headers, rows=data))
        self.printing_plain.append("""  """)
        self.printing_plain.setFontPointSize(12)
        self.printing_plain.append(foot)
        self.printing_plain.setAlignment(Qt.AlignmentFlag.AlignLeft)


    def print_file(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.printing_plain.print(printer)
            self.canceled()

    def canceled(self):
        self.close()

