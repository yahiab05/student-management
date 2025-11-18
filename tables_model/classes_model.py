from PyQt6.QtCore import Qt, QAbstractTableModel
from sqlalchemy import and_
from app.models import Classes, ClassEleve, Students

class ClassesTableModel(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.classes = []  # Store the fetched data
        self.headers = ["ID", "الاسم", "طريقة التدريس", "المعلم", "ملاحظة", "المبلغ", "مقابل", "عدد الحصص", "حصّة المعلم"]

        self.refresh()

    def refresh(self, teacher=None, name=None):
        """Fetch classes from the database and update the model."""
        filters = []
        if name is not None:
            filters.append(Classes.name.ilike(f"%{name}%"))

        if teacher is not None:
            filters.append(Classes.teacher.ilike(f"%{teacher}%"))
       
        self.beginResetModel()
        self.classes = self.session.query(Classes).filter(and_(*filters)).order_by(Classes.name).all()
        self.endResetModel()

        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return len(self.classes) if self.classes else 0

    def columnCount(self, parent=None):
        return len(self.headers)  # Adjust based on your columns

    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        class_obj = self.classes[index.row()]
        column = index.column()

        if column == 0:
            return class_obj.id
        elif column == 1:
            return class_obj.name
        elif column == 2:
            return class_obj.way
        elif column == 3:
            return class_obj.teacher
        elif column == 4:
            return class_obj.note
        elif column == 5:
            return class_obj.price
        elif column == 6:
            return class_obj.exchange
        elif column == 7:
            return class_obj.seance
        elif column == 8:
            return class_obj.teacher_part
        elif column == 9:
            return class_obj.user
        return None

    def headerData(self, section, orientation, role):

        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]

        return None
    
class ClasseleveTableModel(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.classeseleve = []  # Store the fetched data
        self.intro = ""
        self.headers = ["ID", "الاسم", "رقم التسجيل", "القسم", "تاريخ آلتسجيل", "تاريخ الميلاد", "رقم الهاتف", "المستخدم"]

    def refresh(self, class_name=None):
        class_name = None if class_name == "" else class_name
        if class_name is not None:
            self.intro = "قائمة تلاميذ القسم: " + str(class_name)
            query = (
            self.session.query(
                ClassEleve.id,
                Students.name,
                Students.num_inscrit,
                ClassEleve.class_name,
                Students.date_inscrit,  # Assuming this field exists
                Students.birthday ,
                Students.num_tel,
                Students.user
            )
            .join(Students, ClassEleve.student_id == Students.num_inscrit)
            .filter(ClassEleve.class_name == class_name)
        )
        
            query = query.filter(ClassEleve.class_name == class_name)

            self.beginResetModel()
            self.classeseleve = query.order_by(Students.name).all()
            self.endResetModel()

            self.layoutChanged.emit()

        else:
            self.beginResetModel()
            self.classeseleve = []
            self.endResetModel()

            self.layoutChanged.emit()          

    def rowCount(self, parent=None):
        return len(self.classeseleve) if self.classeseleve else 0

    def columnCount(self, parent=None):
        return len(self.headers)  # Adjust based on your columns

    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        class_obj = self.classeseleve[index.row()]
        column = index.column()

        if column == 0:
            return class_obj[0]
        elif column == 1:
            return class_obj[1]
        elif column == 2:
            return class_obj[2]
        elif column == 3:
            return class_obj[3]
        elif column == 4:
            return class_obj[4].strftime("%Y-%m-%d") if class_obj[4] else ""
        elif column == 5:
            return class_obj[5].strftime("%Y-%m-%d") if class_obj[5] else ""
        elif column == 6:
            return class_obj[6]
        elif column == 7:
            return class_obj[7]
        return None
    
    def headerData(self, section, orientation, role):

        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]

        return None