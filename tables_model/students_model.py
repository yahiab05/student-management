from sqlalchemy import and_
from PyQt6.QtCore import Qt, QAbstractTableModel
from sqlalchemy.orm import joinedload
from app.models import Students, StudentsHistory
from datetime import date

class StudentsTableModel(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()
        self.session = session

        self.students = []

        self.headers = ["ID", "Name", "date inscrit", "Birthday", "gender", "parent", "Phone", "cin", 
                        'excused', "activity", "note", "user"]
        
        self.intro = ""
        
        self.refresh()

    def refresh(self, name=None, du=None, au=None, excused="لا", activity="فاعل", gender = None):
        filters = []

        if name is not None:
            filters.append(Students.name.contains(name))
        if du is None:
            du = date(2000, 1, 1)
        if au is None:
            au = date.today() 

        filters.append(Students.birthday.between(du, au))
        if not (du.strftime("%Y-%m-%d") == "2000-01-01" and au == date.today()):
            self.intro = """ بين  """ + du.strftime("%Y-%m-%d") + "  و  " + au.strftime("%Y-%m-%d") + "\n"
        
        if excused is not None:
            filters.append(Students.excused == excused)
            self.intro += "معفى: " + excused + "\n"

        if gender is not None:
            filters.append(Students.gender == gender)
            self.intro += "جنس: " + gender + "\n"

        if activity is not None:
            filters.append(Students.activity == activity)
            self.intro += "نشاط: " + activity

        self.beginResetModel()
        self.students = self.session.query(Students).filter(and_(*filters)).order_by(Students.name).all()
        self.endResetModel()

        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return len(self.students)
    
    def columnCount(self, parent=None):
        return len(self.headers)
    
    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        class_obj = self.students[index.row()]
        column = index.column()

        if column == 0:
            return class_obj.num_inscrit
        elif column == 1:
            return class_obj.name
        elif column == 2:
            return class_obj.get_date_inscrit()
        elif column == 3:
            return class_obj.get_birthday()
        elif column == 4:
            return class_obj.gender
        elif column == 5:
            return class_obj.parent
        elif column == 6:
            return class_obj.num_tel
        elif column == 7:
            return class_obj.cin
        elif column == 8:
            return class_obj.excused
        elif column == 9:
            return class_obj.activity
        elif column == 10:
            return class_obj.note
        elif column == 11:
            return class_obj.user
        return None
    
    def headerData(self, section, orientation, role):

        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]

        return None
    
class StudentsHistoryTableModel(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()
        self.session = session

        self.students = []

        self.headers = ["ID", "الاسم", "تاريخ التسجيل", "تاريخ الميلاد", "الولي", "رقم الهاتف", "المستخدم"]

        self.refresh()

    def refresh(self, ID=None):
        student_id = ID if ID is not None else 0

        self.intro = "تلميذ برقم الهوية: " + str(student_id)

        self.beginResetModel()

        self.students = self.session.query(StudentsHistory).options(joinedload(StudentsHistory.student)).filter(StudentsHistory.num_inscrit == student_id).all()
        
        self.endResetModel()

    def rowCount(self, parent=None):
        return len(self.students)
    
    def columnCount(self, parent=None):
        return len(self.headers)
    
    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        class_obj = self.students[index.row()]
        column = index.column()

        if column == 0:
            return class_obj.num_inscrit
        elif column == 1:
            return class_obj.student.name
        elif column == 2:
            return class_obj.get_date_inscrit()
        elif column == 3:
            return class_obj.student.get_birthday()
        elif column == 4:
            return class_obj.student.parent
        elif column == 5:
            return class_obj.student.num_tel
        elif column == 6:
            return class_obj.user
        return None
    
    def headerData(self, section, orientation, role):

        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]

        return None
    

class StudentsSearchTableModel(QAbstractTableModel):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.students = []  # Store the fetched data
        self.headers = ["ID", "الاسم"]

        self.refresh()

    def refresh(self, name=None):
        if name is None:
            query = self.session.query(Students)
        else:
            query = self.session.query(Students).filter(Students.name.contains(name))

        self.beginResetModel()

        self.students = query.all()

        self.endResetModel()

        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return len(self.students) if self.students else 0

    def columnCount(self, parent=None):
        return len(self.headers)  # Adjust based on your columns

    def data(self, index, role):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        student = self.students[index.row()]
        column = index.column()

        if column == 0:
            return student.num_inscrit
        elif column == 1:
            return student.name

    def headerData(self, section, orientation, role):

        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]

        return None
    
        