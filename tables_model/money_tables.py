from sqlalchemy import and_, func, union_all
from PyQt6.QtCore import Qt, QAbstractTableModel
from sqlalchemy.orm import joinedload
from app.models import Entery, OutMoney, Bank, Caisse
from datetime import date


class EnteryTableModel(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()

        self.session = session
        self.enteries = []
        self.total_price = 0

        self.headers = ["ID", "الاسم", "التاريخ", "المبلغ", "رقم التوصيل", "نوع الدخل", "طريقة الدفع", "ملاحظة", "المستخدم"]

        self.intro = ""

        self.refresh()

    def refresh(self, operator=None,amount=None, du=None, au=None, way = None, types = None, name = None, code = None):
        filters = []

        if name is not None:
            filters.append(Entery.name.contains(name))
        if du is None:
            du = date(2000, 1, 1)
        if au is None:
            au = date.today() 

        if code is not None:
            filters.append(Entery.code == code)

        filters.append(Entery.addition_date.between(du, au))
        if not (du == date(2000, 1, 1) and au == date.today()):
            if du == au:
                self.intro = "يوم " + du.strftime("%Y-%m-%d")
            else:
                self.intro = """بين """ + du.strftime("%Y-%m-%d") + " و " + au.strftime("%Y-%m-%d")

        if operator is not None:
            if operator == "=":
                filters.append(Entery.price == amount)
            elif operator == ">":
                filters.append(Entery.price > amount)
            elif operator == "<":
                filters.append(Entery.price < amount)
            elif operator == ">=":
                filters.append(Entery.price >= amount)
            elif operator == "<=":
                filters.append(Entery.price <= amount)
        
        if way is not None:
            filters.append(Entery.way == way)

        if types is not None:
            filters.append(Entery.type == types)

        self.beginResetModel()
        self.enteries = self.session.query(Entery).filter(and_(*filters)).order_by(Entery.addition_date.desc()).all()
        self.total_price = self.session.query(func.sum(Entery.price)).filter(and_(*filters)).scalar()
        self.total_price = 0 if self.total_price is None else self.total_price
        self.endResetModel()

        self.layoutChanged.emit()

    def rowCount(self, parent = None):
        return len(self.enteries)
    
    def columnCount(self, parent = None):
        return len(self.headers)
    
    def data(self, index, role = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            income = self.enteries[index.row()]
            if index.column() == 0:
                return income.id
            elif index.column() == 1:
                return income.name
            elif index.column() == 2:
                return income.addition_date.strftime("%Y-%m-%d")
            elif index.column() == 3:
                return income.price
            elif index.column() == 4:
                return income.bill_number
            elif index.column() == 5:
                return income.type
            elif index.column() == 6:
                return income.way
            elif index.column() == 7:
                return income.note
            elif index.column() == 8:
                return income.user
            return None
        
    def headerData(self, section, orientation, role):

        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]

        return None  
    

class OutMoneyTableModel(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()

        self.session = session
        self.outs = []
        self.total_price = 0
        self.intro = ""

        self.headers = ["ID", "الاسم", "التاريخ", "المبلغ", "رقم التوصيل", "نوع المصروف", "طريقة الدفع", "ملاحظة", "المستخدم"]

        self.refresh()

    def refresh(self, operator=None,amount=None, du=None, au=None, way = None, types = None, name = None, code= None):
        filters = []

        if name is not None:
            filters.append(OutMoney.name == name)
        if du is None:
            du = date(2000, 1, 1)
        if au is None:
            au = date.today() 

        if code is not None:
            filters.append(OutMoney.code == code)

        filters.append(OutMoney.date.between(du, au))
        if not (du == date(2000, 1, 1) and au == date.today()):
            if du == au:
                self.intro = "يوم " + du.strftime("%Y-%m-%d")
            else:
                self.intro = """بين """ + du.strftime("%Y-%m-%d") + " و " + au.strftime("%Y-%m-%d")

        if operator is not None:
            if operator == "=":
                filters.append(OutMoney.price == amount)
            elif operator == ">":
                filters.append(OutMoney.price > amount)
            elif operator == "<":
                filters.append(OutMoney.price < amount)
            elif operator == ">=":
                filters.append(OutMoney.price >= amount)
            elif operator == "<=":
                filters.append(OutMoney.price <= amount)
        
        if way is not None:
            filters.append(OutMoney.way == way)

        if types is not None:
            filters.append(OutMoney.type == types)

        self.beginResetModel()
        self.outs = self.session.query(OutMoney).filter(and_(*filters)).order_by(OutMoney.date.desc()).all()
        self.total_price = self.session.query(func.sum(OutMoney.price)).filter(and_(*filters)).scalar()
        self.total_price = self.total_price if self.total_price is not None else 0
        self.endResetModel()

        self.layoutChanged.emit()

    def rowCount(self, parent = None):
        return len(self.outs)
    
    def columnCount(self, parent = None):
        return len(self.headers)
    
    def data(self, index, role = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            out = self.outs[index.row()]
            if index.column() == 0:
                return out.id
            elif index.column() == 1:
                return out.name
            elif index.column() == 2:
                return out.date.strftime("%Y-%m-%d")
            elif index.column() == 3:
                return out.price
            elif index.column() == 4:
                return out.bill_num
            elif index.column() == 5:
                return out.type
            elif index.column() == 6:
                return out.way
            elif index.column() == 7:
                return out.note
            elif index.column() == 8:
                return out.user    
            return None
        
    def headerData(self, section, orientation, role):

        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]

        return None
    

class BalanceTableModel(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()

        self.session = session
        self.balances = []
        self.balance = 0
        self.total_income = 0
        self.total_expenses = 0
        self.intro = ""

        self.headers = ["الاسم", "المصاريف", "المداخيل", "التاريخ", "طريقة الدفع"]

        self.refresh()

    def refresh(self, operator=None, amount=None, du=None, au=None, way=None):
        filters_income = []
        filters_expenses = []

        if du is None:
            du = date(2000, 1, 1)
        if au is None:
            au = date.today() 

        filters_income.append(Entery.addition_date.between(du, au))
        filters_expenses.append(OutMoney.date.between(du, au))
        if not (du == date(2000, 1, 1) and au == date.today()):
            self.intro = """بين """ + du.strftime("%Y-%m-%d") + " و " + au.strftime("%Y-%m-%d")

        if operator is not None and amount is not None:
            if operator == "=":
                filters_income.append(Entery.price == amount)
                filters_expenses.append(OutMoney.price == amount)
            elif operator == ">":
                filters_income.append(Entery.price > amount)
                filters_expenses.append(OutMoney.price > amount)
            elif operator == "<":
                filters_income.append(Entery.price < amount)
                filters_expenses.append(OutMoney.price < amount)
            elif operator == ">=":
                filters_income.append(Entery.price >= amount)
                filters_expenses.append(OutMoney.price >= amount)
            elif operator == "<=":
                filters_income.append(Entery.price <= amount)
                filters_expenses.append(OutMoney.price <= amount)

        if way is not None:
            filters_income.append(Entery.way == way)
            filters_expenses.append(OutMoney.way == way)

        income = self.session.query(
            Entery.name.label("name"),
            Entery.price.label("income"),
            func.coalesce(0, '').label("expenses"),
            Entery.way.label("way"),
            Entery.addition_date.label("date")
        ).filter(and_(*filters_income))

        expenses = self.session.query(
            OutMoney.name.label("name"),
            func.coalesce(0, '').label("income"),
            OutMoney.price.label("expenses"),
            OutMoney.way.label("way"),
            OutMoney.date.label("date")
        ).filter(and_(*filters_expenses))
        
        combined_query = union_all(income, expenses)

        self.beginResetModel()
        self.balances = self.session.query(
            combined_query.c.name, combined_query.c.income, combined_query.c.expenses, combined_query.c.way, combined_query.c.date
        ).order_by(combined_query.c.date).all()

        self.total_expenses = self.session.query(func.sum(OutMoney.price)).filter(and_(*filters_expenses)).scalar()
        self.total_income = self.session.query(func.sum(Entery.price)).filter(and_(*filters_income)).scalar()

        self.total_expenses = self.total_expenses if self.total_expenses is not None else 0
        self.total_income = self.total_income if self.total_income is not None else 0

        self.balance = self.total_income - self.total_expenses

        self.endResetModel()

        self.layoutChanged.emit()

    def rowCount(self, parent = None):
        return len(self.balances)
    
    def columnCount(self, parent = None):
        return len(self.headers)
    
    def data(self, index, role = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            balances = self.balances[index.row()]
            if index.column() == 0:
                return balances.name
            elif index.column() == 1:
                return balances.income
            elif index.column() == 2:
                return balances.expenses
            elif index.column() == 3:
                return balances.date.strftime("%Y-%m-%d")
            elif index.column() == 4:
                return balances.way 
            return None
        
    def headerData(self, section, orientation, role):

        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]

        return None
    
class BankTabelModel(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()

        self.session = session
        self.banks = []
        self.balance = 0
        self.total_income = 0
        self.total_expenses = 0
        self.intro = ""

        self.headers = ["المداخيل", "المصاريف", "التاريخ", "ملاحظة"]

        self.refresh()

    def refresh(self, operatore=None, price= None, from_date= None, to_date= None):
        filters = []

        if operatore is not None and price is not None:
            if operatore == "=":
                filters.append(Bank.income == price)
            elif operatore == ">":
                filters.append(Bank.income > price)
            elif operatore == "<":
                filters.append(Bank.income < price)
            elif operatore == ">=":
                filters.append(Bank.income >= price)
            elif operatore == "<=":
                filters.append(Bank.income <= price)

        if from_date is None:
            from_date = date(2000, 1, 1)
        if to_date is None:
            to_date = date.today() 

        filters.append(Bank.date.between(from_date, to_date))
        if not (from_date == date(2000, 1, 1) and to_date == date.today()):
            self.intro = """بين """ + from_date.strftime("%Y-%m-%d") + " و " + to_date.strftime("%Y-%m-%d")

        self.beginResetModel()
        self.banks = self.session.query(Bank).filter(and_(*filters)).order_by(Bank.date.desc()).all()

        self.total_expenses = self.session.query(func.sum(Bank.expense)).filter(and_(*filters)).scalar()
        self.total_income = self.session.query(func.sum(Bank.income)).filter(and_(*filters)).scalar()
        self.total_expenses = self.total_expenses if self.total_expenses is not None else 0
        self.total_income = self.total_income if self.total_income is not None else 0

        self.balance = self.total_income - self.total_expenses

        self.endResetModel()

    def rowCount(self, parent = None):
        return len(self.banks)
    
    def columnCount(self, parent = None):
        return len(self.headers)
    
    def data(self, index, role = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            bank = self.banks[index.row()]
            if index.column() == 0:
                return bank.income
            elif index.column() == 1:
                return bank.expense
            elif index.column() == 2:
                return bank.date.strftime("%Y-%m-%d")
            elif index.column() == 3:
                return bank.note
            return None
        
    def headerData(self, section, orientation, role):

        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]

        return None
    
class CaisseTabelModel(QAbstractTableModel):    
    def __init__(self, session):
        super().__init__()

        self.session = session
        self.caisse = []
        self.balance = 0
        self.total_income = 0
        self.total_expenses = 0
        self.intro = ""

        self.headers = ["المداخيل", "المصاريف", "التاريخ", "ملاحظة"]

        self.refresh()

    def refresh(self, operatore=None, price= None, from_date= None, to_date= None):
        filters = []

        if operatore is not None and price is not None:
            if operatore == "=":
                filters.append(Caisse.income == price)
            elif operatore == ">":
                filters.append(Caisse.income > price)
            elif operatore == "<":
                filters.append(Caisse.income < price)
            elif operatore == ">=":
                filters.append(Caisse.income >= price)
            elif operatore == "<=":
                filters.append(Caisse.income <= price)

        if from_date is None:
            from_date = date(2000, 1, 1)
        if to_date is None:
            to_date = date.today() 

        filters.append(Caisse.date.between(from_date, to_date))
        if not (from_date == date(2000, 1, 1) and to_date == date.today()):
            self.intro = """بين """ + from_date.strftime("%Y-%m-%d") + " و " + to_date.strftime("%Y-%m-%d")

        self.beginResetModel()
        self.caisse = self.session.query(Caisse).filter(and_(*filters)).order_by(Caisse.date.desc()).all()

        self.total_expenses = self.session.query(func.sum(Caisse.expense)).filter(and_(*filters)).scalar()
        self.total_income = self.session.query(func.sum(Caisse.income)).filter(and_(*filters)).scalar()
        self.total_expenses = self.total_expenses if self.total_expenses is not None else 0
        self.total_income = self.total_income if self.total_income is not None else 0

        self.balance = self.total_income - self.total_expenses

        self.endResetModel()

        self.layoutChanged.emit()

    def rowCount(self, parent = None):
        return len(self.caisse)
    
    def columnCount(self, parent = None):
        return len(self.headers)
    
    def data(self, index, role = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            caisse = self.caisse[index.row()]
            if index.column() == 0:
                return caisse.income
            elif index.column() == 1:
                return caisse.expense
            elif index.column() == 2:
                return caisse.date.strftime("%Y-%m-%d")
            elif index.column() == 3:
                return caisse.note
            return None
        
    def headerData(self, section, orientation, role):

        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]

        return None