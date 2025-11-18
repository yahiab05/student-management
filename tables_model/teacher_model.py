from PyQt6.QtCore import Qt, QAbstractTableModel
from sqlalchemy.orm import joinedload
from app.models import Teachers, TeachersHistory


class TeachersTableModel(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()

        self.session = session

        self.teachers = []

        self.headers = ["ID", "الاسم", "تاريخ التسجيل", "تاريخ الميلاد", "رقم الهاتف", "بمقابل", "المستخدم" ]
        self.refresh()

    def refresh(self, name=None):
        teacher = name if name is not None else None

        self.beginResetModel()

        query = self.session.query(Teachers)

        if teacher is not None:
            query = query.filter(Teachers.name.contains(teacher))

        self.teachers = query.order_by(Teachers.name).all()

        self.endResetModel()

        self.layoutChanged.emit()
    
    def rowCount(self, parent=None):
        return len(self.teachers) if self.teachers else 0

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        class_obj = self.teachers[index.row()]
        column = index.column()

        if column == 0:
            return class_obj.id
        elif column == 1:
            return class_obj.name
        elif column == 2:
            return class_obj.get_date_inscrit()
        elif column == 3:
            return class_obj.get_birthday()
        elif column == 4:
            return class_obj.phone
        elif column == 5:
            return class_obj.payed
        elif column == 6:
            return class_obj.note
        elif column == 7:
            return class_obj.user
        return None

    def headerData(self, section, orientation, role):

        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]

        return None
    

class TeachersHistoryTableModel(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()

        self.session = session

        self.teachers = []
        

        self.headers = ["ID", "الاسم", "سنوات التدريس", "تاريخ الميلاد", "بمقابل", "المستخدم" ]
        self.refresh()

    def refresh(self, ID=None):
        identifier = ID if ID is not None else None

        self.beginResetModel()

        query = self.session.query(TeachersHistory).options(joinedload(TeachersHistory.teacher))


        if identifier is not None:
            query = query.filter(TeachersHistory.teacher_id == identifier)

        self.teachers = query.all()

        self.endResetModel()

        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return len(self.teachers) if self.teachers else 0

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        class_obj = self.teachers[index.row()]
        column = index.column()

        if column == 0:
            return class_obj.teacher_id
        elif column == 1:
            return class_obj.teacher.name
        elif column == 2:
            return class_obj.get_date_inscrit()
        elif column == 3:
            return class_obj.teacher.get_birthday()
        elif column == 4:
            return class_obj.payed
        elif column == 5:
            return class_obj.user
        return None

    def headerData(self, section, orientation, role):

        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]

        return None


class TeacherSearchTableModel(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()

        self.session = session

        self.teachers = []

        self.headers = ["ID", "الاسم"]

        self.refresh()

    def refresh(self, name=None):
        teacher = name if name else None

        self.beginResetModel()

        query = self.session.query(Teachers)

        if teacher is not None:
            query = query.filter(Teachers.name.contains(teacher))

        self.teachers = query.all()

        self.endResetModel()

        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return len(self.teachers) if self.teachers else 0

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        class_obj = self.teachers[index.row()]
        column = index.column()

        if column == 0:
            return class_obj.id
        elif column == 1:
            return class_obj.name
        return None

    def headerData(self, section, orientation, role):

        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]

        return None