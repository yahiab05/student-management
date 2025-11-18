from datetime import date
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Float, Time
from sqlalchemy.orm import relationship
from PyQt6.QtCore import QDate, QTime
from .database import Base

class Role(Base):
    __tablename__ = "role"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    classes = Column(Boolean, nullable=False)
    students = Column(Boolean, nullable=False)
    teachers = Column(Boolean, nullable=False)
    payment = Column(Boolean, nullable=False)
    money = Column(Boolean, nullable=False)
    absent = Column(Boolean, nullable=False)
    settings = Column(Boolean, nullable=False)
    user = Column(Boolean, nullable=False)
    payment_editting = Column(Boolean, nullable=False)


    def __repr__(self):
        return f"Role(id={self.id}, name={self.name}, classes={self.classes}, students={self.students}, teachers={self.teachers}, parents={self.parents})"


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}



    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role_name = Column(String(255), ForeignKey("role.name"))

    role = relationship("Role", backref="users", lazy=True)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, password={self.password})"
    

class Students(Base):
    __tablename__ = "students"
    __table_args__ = {"extend_existing": True}


    num_inscrit = Column(Integer, primary_key=True, index=True) 
    name = Column(String(255), nullable=False)
    gender = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=False)
    date_inscrit = Column(Date, nullable=False)
    parent = Column(String(255), nullable=False)
    cin = Column(Integer, nullable=False)
    activity = Column(String(255), nullable=False)
    num_tel = Column(String(255), nullable=False)
    excused = Column(String(255), nullable=False)
    note = Column(String(255), nullable=False)
    user = Column(String(255), nullable=False)

    courses = relationship("Classes", secondary='classeleve', back_populates="students")

    def __repr__(self):
        return f"Student {self.num_inscrit}"
    
    def set_birthday(self, date: QDate):
        return date.toPyDate()

    def get_birthday(self):
        return QDate.fromString(str(self.birthday), "yyyy-MM-dd")
    
    def set_date_inscrit(self, date: QDate):
        return date.toPyDate()

    def get_date_inscrit(self):
        return QDate.fromString(str(self.date_inscrit), "yyyy-MM-dd")
    
class StudentsHistory(Base):
    __tablename__ = "students_history"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True) 
    num_inscrit = Column(Integer, ForeignKey("students.num_inscrit", ondelete="CASCADE"))
    date_inscrit = Column(Date, nullable=False)
    user = Column(String(255), nullable=False)

    def set_date_inscrit(self, date: QDate):
        return date.toPyDate()

    def get_date_inscrit(self):
        return QDate.fromString(str(self.date_inscrit), "yyyy-MM-dd")

    student = relationship("Students", backref="students_history")
    

class Classes(Base):
    __tablename__ = "classes"
    __table_args__ = {"extend_existing": True}


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    way = Column(String(255), nullable=False)
    teacher = Column(String(255), nullable=False)
    note = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    user = Column(String(255), nullable=False)
    seance = Column(Integer, nullable=False)
    exchange = Column(String(255), nullable=False)
    teacher_part = Column(Float, nullable=False)

    students = relationship("Students", secondary="classeleve", back_populates="courses")

    def __repr__(self):
        return f"Class(id={self.id}, name={self.name}, way={self.way}, teacher={self.teacher}, price={self.price})"
    
class Teachers(Base):
    __tablename__ = "teachers"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    date_inscrit = Column(Date, nullable=False)
    birthday = Column(Date, nullable=False)
    phone = Column(String(255), nullable=False)
    note = Column(String(255), nullable=False)
    payed = Column(String(255), nullable=False)
    user = Column(String(255), nullable=False)

    def set_birthday(self, date: QDate):
        return date.toPyDate()

    def get_birthday(self):
        return QDate.fromString(str(self.birthday), "yyyy-MM-dd")
    
    def set_date_iscrit(self, date: QDate):
        return date.toPyDate()

    def get_date_inscrit(self):
        return QDate.fromString(str(self.date_inscrit), "yyyy-MM-dd")
    
class TeachersHistory(Base):
    __tablename__ = "teachershistory"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    date_inscrit = Column(Date, nullable=False)
    payed = Column(String(255), nullable=False)
    user = Column(String(255), nullable=False)

    def set_date_inscrit(self, date: QDate):
        return date.toPyDate()
    
    def get_date_inscrit(self):
        return QDate.fromString(str(self.date_inscrit), "yyyy-MM-dd")

    teacher = relationship("Teachers", backref="teachershistory")
    
class ClassEleve(Base):
    __tablename__ = "classeleve"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.num_inscrit", ondelete="CASCADE"))
    class_name = Column(String(255), ForeignKey("classes.name"))


class Settings(Base):
    __tablename__ = "settings"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    way_teaching = Column(String(255), unique=True)
    entery = Column(String(255), unique=True)
    entery_code = Column(Integer, unique=True)
    out_money = Column(String(255), unique=True)
    out_code = Column(Integer, unique=True)
    way_payment = Column(String(255), unique=True)
    fr = Column(String(255), unique=True)


class OutMoney(Base):
    __tablename__ = "outmoney"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    bill_num = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    price = Column(Float, nullable=False)
    way = Column(String(255), nullable=False)	
    cheq_num = Column(Integer)
    note = Column(String(255),  nullable=False)
    code = Column(Integer, nullable=False)
    type = Column(String(255), nullable=False)
    user = Column(String(255), nullable=False)

    def __repr__(self):
        return f"OutMoney(id={self.id}, name={self.name}, bill_num={self.bill_num}, date={self.date}, price={self.price})"
    
    def set_date(self, date: QDate):
        return date.toPyDate()

    def get_date(self):
        return QDate.fromString(self.date.strftime("%Y-%m-%d"), "yyyy-MM-dd")

class Entery(Base):
    __tablename__ = "entery"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    num_inscrit = Column(Integer)
    name = Column(String(255), nullable=False)
    bill_number = Column(Integer, nullable=False)
    payment_date = Column(Date)
    addition_date = Column(Date, nullable=False)
    way = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False) 
    code = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    note = Column(String(255))
    user = Column(String(255), nullable=False)
    cheq_num = Column(Integer)
    classroom = Column(String(255))

    def __repr__(self):
        return f"Entery(id={self.id}, date={self.date}, type={self.type}, code={self.code}, price={self.price})"
    
    def set_add_date(self, date: QDate):
        return date.toPyDate()

    def get_add_date(self):
        return QDate.fromString(self.addition_date.strftime("%Y-%m-%d"), "yyyy-MM-dd")
    
    def set_payment_date(self, date: QDate):
        return date.toPyDate()

    def get_payment_date(self):
        return QDate.fromString(self.payment_date.strftime("%Y-%m"), "yyyy-MM")


class Caisse(Base):
    __tablename__ = "caisse"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    income_id = Column(Integer)
    expense_id = Column(Integer)
    income = Column(Float, nullable=True)
    expense = Column(Float, nullable=True)
    date = Column(Date, nullable=False)
    note = Column(String(255), nullable=False)

    def set_date(self, date: QDate):
        return date.toPyDate()
    
    def get_date(self):
        return QDate.fromString(self.date.strftime("%Y-%m-%d"), "yyyy-MM-dd")

class Bank(Base):
    __tablename__ = "bank"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    income_id = Column(Integer)
    expense_id = Column(Integer)
    income = Column(Float, nullable=True)
    expense = Column(Float, nullable=True)
    date = Column(Date, nullable=False)
    note = Column(String(255), nullable=False)

    def set_date(self, date: QDate):
        return date.toPyDate()
    
    def get_date(self):
        return QDate.fromString(self.date.strftime("%Y-%m-%d"), "yyyy-MM-dd")
    

class AbsentT(Base):
    __tablename__ = "absent_t"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    num_inscrit = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    class_ab = Column(String(255), nullable=False)
    date_ab = Column(Date, nullable=False)
    du = Column(Time, nullable=False)
    time_last = Column(Time, nullable=False)
    rep = Column(String(255))
    date_rep = Column(Date)
    user = Column(String(255), nullable=False)

    teacher = relationship("Teachers", backref="absent_t", lazy=True)

    def set_date(self, date: QDate):
        return date.toPyDate()

    def get_date(self):
        return QDate.fromString(self.date_ab.strftime("%Y-%m-%d"), "yyyy-MM-dd")
    
    def set_time(self, time: QTime):
        return time.toPyTime()

    def get_time(self):
        return QTime.fromString(self.du.strftime("%H:%M"), "HH:mm")
    

class AbsentS(Base):
    __tablename__ = "absent_s"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    num_inscrit = Column(Integer, ForeignKey("students.num_inscrit", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    class_ab = Column(String(255), nullable=False)
    date_ab = Column(Date, nullable=False)
    du = Column(Time, nullable=False)
    time_last = Column(Time, nullable=False)
    user = Column(String(255), nullable=False)

    student = relationship("Students", backref="absent_s", uselist=True)

    def set_date(self, date: QDate):
        return date.toPyDate()

    def get_date(self):
        return QDate.fromString(self.date_ab.strftime("%Y-%m-%d"), "yyyy-MM-dd")
    
    def set_time(self, time: QTime):
        return time.toPyTime()

    def get_time(self):
        return QTime.fromString(self.du.strftime("%H:%M"), "HH:mm")


