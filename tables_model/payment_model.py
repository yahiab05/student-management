from sqlalchemy import and_, func
from PyQt6.QtCore import Qt, QAbstractTableModel
from sqlalchemy.orm import joinedload
from app.models import Entery
from datetime import date


class PaymentTableModel(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()

        self.session = session
        self.payments = []
        self.total_price = 0

        self.headers = ["ID", "رقم الوصل", "الاسم", "رقم التسجيل", "القسم", "مقابل شهر", "أضيف يوم", 
                        "المبلغ","طريقة الدفع", "رقم الصك", "المستخدم"]
        
        self.refresh()

    def refresh(self, classroom=None, du=None, au=None, way = None, num_inscrit = None, name = None):
        filters = []

        classroom = None if classroom == "" else classroom
        way = None if way == "" else way
        name = None if name == "" else name
        num_inscrit = None if num_inscrit == "" else num_inscrit

        if name is not None:
            filters.append(Entery.name == name)     

        if num_inscrit is not None:
            filters.clear()
            filters.append(Entery.num_inscrit == num_inscrit)

        if classroom is not None:
            filters.append(Entery.classroom == classroom)

        if du is None:
            du = date(2000, 1, 1)
        if au is None:
            au = date.today() 

        filters.append(Entery.payment_date.between(du, au))

        if way is not None:
            filters.append(Entery.way == way)

        filters.append(Entery.code == 13)

        self.beginResetModel()
        self.payments = self.session.query(Entery).filter(and_(*filters)).order_by(Entery.name, Entery.payment_date).all()
        self.total_price = self.session.query(func.sum(Entery.price)).filter(and_(*filters)).scalar()
        self.endResetModel()

        self.layoutChanged.emit()

    def rowCount(self, parent = ...):
        return len(self.payments)
    
    def columnCount(self, parent = ...):
        return len(self.headers)
    
    def data(self, index, role = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            payment = self.payments[index.row()]
            if index.column() == 0:
                return payment.id
            elif index.column() == 1:
                return payment.bill_number
            elif index.column() == 2:
                return payment.name
            elif index.column() == 3:
                return payment.num_inscrit
            elif index.column() == 4:
                return payment.classroom
            elif index.column() == 5:
                return payment.payment_date.strftime("%Y-%m")
            elif index.column() == 6:
                return payment.addition_date.strftime("%Y-%m-%d")
            elif index.column() == 7:
                return payment.price
            elif index.column() == 8:
                return payment.way
            elif index.column() == 9:
                return payment.cheq_num
            elif index.column() == 10:
                return payment.user
            return None
        
    def headerData(self, section, orientation, role):

        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]

        return None            
    