from PyQt6.QtCore import Qt, QAbstractTableModel
from sqlalchemy.orm import joinedload
from app.models import AbsentS, AbsentT, Teachers, Students
from datetime import date
from sqlalchemy import and_


class AbsentTeacherTableModel(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()

        self.session = session

        self.absents = []

        self.headers = ["ID", "الاسم", "القسم", "التاريخ", "من", "الى", "معوض", "تاريخ التعويض", "رقم الهاتف", "المستخدم"]
        self.intro = ""

        self.refresh()

    def refresh(self, name = None, classroom = None, replacement = None, from_date = None, to_date = None):
        filters = []

        if name is not None:
            filters.append(Teachers.name == name)

        if classroom is not None:
            filters.append(AbsentT.class_ab == classroom)

        if replacement is not None:
            filters.append(AbsentT.rep == replacement)

        if from_date is None:
            from_date = date(2000, 1, 1)
        if to_date is None:
            to_date = date.today() 

        filters.append(AbsentT.date_ab.between(from_date, to_date))
        if not (from_date == date(2000, 1, 1) and to_date == date.today().isoformat()):
            self.intro= """ بين  """ + from_date.strftime("%Y-%m-%d") + "  و  " + to_date.strftime("%Y-%m-%d")

        self.beginResetModel()
        self.absents = self.session.query(AbsentT).join(Teachers, Teachers.id == AbsentT.num_inscrit).options(joinedload(AbsentT.teacher)).filter(and_(*filters)).order_by(AbsentT.date_ab.desc()).all()
        self.endResetModel()

        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return len(self.absents)
    
    def columnCount(self, parent=None):
        return len(self.headers)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            abs = self.absents[index.row()]
            if index.column() == 0:
                return abs.id
            elif index.column() == 1:
                return abs.teacher.name
            elif index.column() == 2:
                return abs.class_ab
            elif index.column() == 3:
                return abs.date_ab.strftime("%Y-%m-%d")
            elif index.column() == 4:
                return abs.du.strftime("%H:%M")
            elif index.column() == 5:
                return abs.time_last.strftime("%H:%M")
            elif index.column() == 6:
                return abs.rep
            elif index.column() == 7:
                return "" if abs.date_rep is None else abs.date_rep.strftime("%Y-%m-%d")
            elif index.column() == 8:
                return abs.teacher.phone
            elif index.column() == 9:
                return abs.user
        return None
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section]
        return None
    

class AbsentStudentTableModel(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()

        self.session = session

        self.absents = []

        self.headers = ["ID", "الاسم", "القسم", "التاريخ", "من", "الى", "رقم الهاتف", "المستخدم"]

        self.intro = ""

        self.refresh()

    def refresh(self, name = None, classroom = None, from_date = None, to_date = None):
        filters = []

        if name is not None:
            filters.append(Students.name == name)

        if classroom is not None:
            filters.append(AbsentS.class_ab == classroom)

        if from_date is None:
            from_date = date(2000, 1, 1)
        if to_date is None:
            to_date = date.today() 

        if not (from_date.strftime("%Y-%m-%d") == "2000-01-01" and to_date == date.today()):
            self.intro = """ بين  """ + from_date.strftime("%Y-%m-%d") + "  و  " + to_date.strftime("%Y-%m-%d")

        filters.append(AbsentS.date_ab.between(from_date, to_date))

        self.beginResetModel()
        self.absents = self.session.query(AbsentS).options(joinedload(AbsentS.student)).filter(and_(*filters)).order_by(AbsentS.date_ab.desc()).all()
        self.endResetModel()

        self.layoutChanged.emit()


    def rowCount(self, parent=None):
        return len(self.absents)
    
    def columnCount(self, parent=None):
        return len(self.headers)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            abs = self.absents[index.row()]
            if index.column() == 0:
                return abs.id
            elif index.column() == 1:
                return abs.student.name
            elif index.column() == 2:
                return abs.class_ab
            elif index.column() == 3:
                return abs.date_ab.strftime("%Y-%m-%d")
            elif index.column() == 4:
                return abs.du.strftime("%H:%M")
            elif index.column() == 5:
                return abs.time_last.strftime("%H:%M")
            elif index.column() == 6:
                return abs.student.num_tel
            elif index.column() == 7:
                return abs.user
        return None
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section]
        return None