# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'students.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QDateEdit,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTableView, QVBoxLayout,
    QWidget)

class Ui_students(object):
    def setupUi(self, students):
        if not students.objectName():
            students.setObjectName(u"students")
        students.setWindowModality(Qt.WindowModality.WindowModal)
        students.resize(1186, 605)
        self.horizontalLayout_2 = QHBoxLayout(students)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(students)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.search_by_name = QLineEdit(self.frame_4)
        self.search_by_name.setObjectName(u"search_by_name")
        self.search_by_name.setMinimumSize(QSize(100, 30))
        font = QFont()
        font.setPointSize(15)
        self.search_by_name.setFont(font)
        self.search_by_name.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.search_by_name.setStyleSheet(u"border: 3px solid black;\n"
"border-left: none;\n"
"border-right: none;\n"
"border-top: none \n"
"")

        self.horizontalLayout.addWidget(self.search_by_name)

        self.label_10 = QLabel(self.frame_4)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_10)

        self.maximize = QPushButton(self.frame_4)
        self.maximize.setObjectName(u"maximize")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.maximize.sizePolicy().hasHeightForWidth())
        self.maximize.setSizePolicy(sizePolicy1)
        self.maximize.setMinimumSize(QSize(25, 25))
        self.maximize.setMaximumSize(QSize(25, 25))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.maximize.setFont(font1)

        self.horizontalLayout.addWidget(self.maximize)


        self.verticalLayout_6.addWidget(self.frame_4)

        self.student_tab = QTableView(self.frame)
        self.student_tab.setObjectName(u"student_tab")
        self.student_tab.setFont(font)
        self.student_tab.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.student_tab.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.student_tab.setAlternatingRowColors(True)
        self.student_tab.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.student_tab.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.student_tab.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.student_tab.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.student_tab.setShowGrid(False)
        self.student_tab.horizontalHeader().setMinimumSectionSize(150)
        self.student_tab.verticalHeader().setDefaultSectionSize(35)

        self.verticalLayout_6.addWidget(self.student_tab)

        self.frame_7 = QFrame(self.frame)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.printing_btn = QPushButton(self.frame_7)
        self.printing_btn.setObjectName(u"printing_btn")
        self.printing_btn.setMinimumSize(QSize(150, 30))
        self.printing_btn.setFont(font)
        self.printing_btn.setStyleSheet(u"background-color: rgb(0, 255, 255);")

        self.horizontalLayout_5.addWidget(self.printing_btn)

        self.export_btn = QPushButton(self.frame_7)
        self.export_btn.setObjectName(u"export_btn")
        self.export_btn.setMinimumSize(QSize(150, 30))
        self.export_btn.setFont(font)
        self.export_btn.setStyleSheet(u"background-color: rgb(127, 255, 67);")

        self.horizontalLayout_5.addWidget(self.export_btn)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)

        self.reset_btn = QPushButton(self.frame_7)
        self.reset_btn.setObjectName(u"reset_btn")
        self.reset_btn.setMinimumSize(QSize(150, 30))
        self.reset_btn.setFont(font)
        self.reset_btn.setStyleSheet(u"background-color: rgb(252, 73, 60);")

        self.horizontalLayout_5.addWidget(self.reset_btn)

        self.search_btn = QPushButton(self.frame_7)
        self.search_btn.setObjectName(u"search_btn")
        self.search_btn.setMinimumSize(QSize(150, 30))
        self.search_btn.setFont(font)
        self.search_btn.setStyleSheet(u"background-color: rgb(94, 197, 93);")

        self.horizontalLayout_5.addWidget(self.search_btn)


        self.verticalLayout_6.addWidget(self.frame_7)


        self.horizontalLayout_2.addWidget(self.frame)

        self.search_frame = QFrame(students)
        self.search_frame.setObjectName(u"search_frame")
        self.search_frame.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.search_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.search_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.search_frame)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.minimize = QPushButton(self.search_frame)
        self.minimize.setObjectName(u"minimize")
        sizePolicy1.setHeightForWidth(self.minimize.sizePolicy().hasHeightForWidth())
        self.minimize.setSizePolicy(sizePolicy1)
        self.minimize.setMinimumSize(QSize(25, 25))
        self.minimize.setMaximumSize(QSize(25, 25))
        self.minimize.setFont(font1)

        self.verticalLayout_8.addWidget(self.minimize)

        self.groupBox = QGroupBox(self.search_frame)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.groupBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.in_class = QComboBox(self.groupBox)
        self.in_class.addItem("")
        self.in_class.addItem("")
        self.in_class.setObjectName(u"in_class")
        self.in_class.setMinimumSize(QSize(0, 30))
        self.in_class.setFont(font)
        self.in_class.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.in_class.setEditable(False)

        self.verticalLayout.addWidget(self.in_class)


        self.verticalLayout_8.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.search_frame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.du = QDateEdit(self.groupBox_2)
        self.du.setObjectName(u"du")
        self.du.setFont(font)
        self.du.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.du.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.du.setCalendarPopup(True)

        self.verticalLayout_2.addWidget(self.du)

        self.to = QDateEdit(self.groupBox_2)
        self.to.setObjectName(u"to")
        self.to.setFont(font)
        self.to.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.to.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.to.setCalendarPopup(True)

        self.verticalLayout_2.addWidget(self.to)


        self.verticalLayout_8.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.search_frame)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.excused_search = QComboBox(self.groupBox_3)
        self.excused_search.addItem("")
        self.excused_search.addItem("")
        self.excused_search.setObjectName(u"excused_search")
        self.excused_search.setMinimumSize(QSize(0, 30))
        self.excused_search.setFont(font)
        self.excused_search.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.excused_search.setEditable(False)

        self.verticalLayout_3.addWidget(self.excused_search)


        self.verticalLayout_8.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.search_frame)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.activity_search = QComboBox(self.groupBox_4)
        self.activity_search.addItem("")
        self.activity_search.addItem("")
        self.activity_search.setObjectName(u"activity_search")
        self.activity_search.setMinimumSize(QSize(100, 30))
        self.activity_search.setFont(font)
        self.activity_search.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.activity_search.setEditable(False)

        self.verticalLayout_4.addWidget(self.activity_search)


        self.verticalLayout_8.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.search_frame)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.nb = QLabel(self.groupBox_5)
        self.nb.setObjectName(u"nb")
        self.nb.setMinimumSize(QSize(50, 0))
        self.nb.setMaximumSize(QSize(16777215, 50))
        self.nb.setFont(font)
        self.nb.setStyleSheet(u"border: 3px solid black; \n"
"border-radius: 15px")
        self.nb.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.nb)


        self.verticalLayout_8.addWidget(self.groupBox_5)


        self.horizontalLayout_2.addWidget(self.search_frame)

        self.frame_2 = QFrame(students)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.name = QLineEdit(self.frame_2)
        self.name.setObjectName(u"name")
        self.name.setFont(font)
        self.name.setStyleSheet(u"border: 3px solid black;\n"
"border-left: none;\n"
"border-right: none;\n"
"border-top: none \n"
"")

        self.gridLayout.addWidget(self.name, 1, 0, 1, 2)

        self.label_7 = QLabel(self.frame_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.gridLayout.addWidget(self.label_7, 7, 2, 1, 1)

        self.birthday = QDateEdit(self.frame_2)
        self.birthday.setObjectName(u"birthday")
        self.birthday.setFont(font)
        self.birthday.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.birthday.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.birthday.setCalendarPopup(True)

        self.gridLayout.addWidget(self.birthday, 2, 0, 1, 2)

        self.gender = QComboBox(self.frame_2)
        self.gender.addItem("")
        self.gender.addItem("")
        self.gender.setObjectName(u"gender")
        self.gender.setMinimumSize(QSize(0, 30))
        self.gender.setFont(font)
        self.gender.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.gender.setEditable(False)

        self.gridLayout.addWidget(self.gender, 3, 0, 1, 1)

        self.label_6 = QLabel(self.frame_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.gridLayout.addWidget(self.label_6, 5, 2, 1, 1)

        self.num_tel_2 = QLineEdit(self.frame_2)
        self.num_tel_2.setObjectName(u"num_tel_2")
        self.num_tel_2.setFont(font)
        self.num_tel_2.setStyleSheet(u"border: 3px solid black;\n"
"border-left: none;\n"
"border-right: none;\n"
"border-top: none \n"
"")

        self.gridLayout.addWidget(self.num_tel_2, 6, 0, 1, 2)

        self.add_btn = QPushButton(self.frame_2)
        self.add_btn.setObjectName(u"add_btn")
        self.add_btn.setMinimumSize(QSize(120, 30))
        self.add_btn.setMaximumSize(QSize(120, 16777215))
        self.add_btn.setFont(font)
        self.add_btn.setStyleSheet(u"background-color: rgb(95, 199, 94);")

        self.gridLayout.addWidget(self.add_btn, 11, 0, 1, 2)

        self.excused = QComboBox(self.frame_2)
        self.excused.addItem("")
        self.excused.addItem("")
        self.excused.setObjectName(u"excused")
        self.excused.setMinimumSize(QSize(0, 30))
        self.excused.setFont(font)
        self.excused.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.excused.setEditable(False)

        self.gridLayout.addWidget(self.excused, 9, 0, 1, 1)

        self.note = QLineEdit(self.frame_2)
        self.note.setObjectName(u"note")
        self.note.setFont(font)
        self.note.setStyleSheet(u"border: 3px solid black;\n"
"border-left: none;\n"
"border-right: none;\n"
"border-top: none \n"
"")

        self.gridLayout.addWidget(self.note, 10, 0, 1, 2)

        self.update_btn = QPushButton(self.frame_2)
        self.update_btn.setObjectName(u"update_btn")
        self.update_btn.setMinimumSize(QSize(120, 30))
        self.update_btn.setMaximumSize(QSize(120, 16777215))
        self.update_btn.setFont(font)
        self.update_btn.setStyleSheet(u"background-color: rgb(255, 160, 65);")

        self.gridLayout.addWidget(self.update_btn, 12, 0, 1, 2)

        self.label_9 = QLabel(self.frame_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.gridLayout.addWidget(self.label_9, 8, 2, 1, 1)

        self.parent = QLineEdit(self.frame_2)
        self.parent.setObjectName(u"parent")
        self.parent.setFont(font)
        self.parent.setStyleSheet(u"border: 3px solid black;\n"
"border-left: none;\n"
"border-right: none;\n"
"border-top: none \n"
"")

        self.gridLayout.addWidget(self.parent, 4, 0, 1, 2)

        self.new_year = QPushButton(self.frame_2)
        self.new_year.setObjectName(u"new_year")
        self.new_year.setMinimumSize(QSize(120, 30))
        self.new_year.setMaximumSize(QSize(120, 16777215))
        self.new_year.setFont(font)
        self.new_year.setStyleSheet(u"background-color: rgb(255, 0, 255);")

        self.gridLayout.addWidget(self.new_year, 13, 1, 1, 2)

        self.activity = QComboBox(self.frame_2)
        self.activity.addItem("")
        self.activity.addItem("")
        self.activity.setObjectName(u"activity")
        self.activity.setMinimumSize(QSize(0, 30))
        self.activity.setFont(font)
        self.activity.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.activity.setEditable(False)

        self.gridLayout.addWidget(self.activity, 8, 0, 1, 2)

        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.gridLayout.addWidget(self.label_3, 2, 2, 1, 1)

        self.label_12 = QLabel(self.frame_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)

        self.gridLayout.addWidget(self.label_12, 9, 2, 1, 1)

        self.num_tel = QLineEdit(self.frame_2)
        self.num_tel.setObjectName(u"num_tel")
        self.num_tel.setFont(font)
        self.num_tel.setStyleSheet(u"border: 3px solid black;\n"
"border-left: none;\n"
"border-right: none;\n"
"border-top: none \n"
"")

        self.gridLayout.addWidget(self.num_tel, 5, 0, 1, 2)

        self.delete_btn = QPushButton(self.frame_2)
        self.delete_btn.setObjectName(u"delete_btn")
        self.delete_btn.setMinimumSize(QSize(120, 30))
        self.delete_btn.setMaximumSize(QSize(120, 16777215))
        self.delete_btn.setFont(font)
        self.delete_btn.setStyleSheet(u"background-color: rgb(255, 74, 61);")

        self.gridLayout.addWidget(self.delete_btn, 12, 2, 1, 1)

        self.label_5 = QLabel(self.frame_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.gridLayout.addWidget(self.label_5, 4, 2, 1, 1)

        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1)

        self.date_inscrit = QDateEdit(self.frame_2)
        self.date_inscrit.setObjectName(u"date_inscrit")
        self.date_inscrit.setFont(font)
        self.date_inscrit.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.date_inscrit.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.date_inscrit.setCalendarPopup(True)

        self.gridLayout.addWidget(self.date_inscrit, 0, 0, 1, 2)

        self.label_11 = QLabel(self.frame_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.gridLayout.addWidget(self.label_11, 0, 2, 1, 1)

        self.label_16 = QLabel(self.frame_2)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font)

        self.gridLayout.addWidget(self.label_16, 6, 2, 1, 1)

        self.label_18 = QLabel(self.frame_2)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font)

        self.gridLayout.addWidget(self.label_18, 3, 2, 1, 1)

        self.label_17 = QLabel(self.frame_2)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font)

        self.gridLayout.addWidget(self.label_17, 10, 2, 1, 1)

        self.cin = QLineEdit(self.frame_2)
        self.cin.setObjectName(u"cin")
        self.cin.setFont(font)
        self.cin.setStyleSheet(u"border: 3px solid black;\n"
"border-left: none;\n"
"border-right: none;\n"
"border-top: none \n"
"")

        self.gridLayout.addWidget(self.cin, 7, 0, 1, 2)

        self.new_btn = QPushButton(self.frame_2)
        self.new_btn.setObjectName(u"new_btn")
        self.new_btn.setMinimumSize(QSize(120, 30))
        self.new_btn.setMaximumSize(QSize(120, 16777215))
        self.new_btn.setFont(font)
        self.new_btn.setStyleSheet(u"background-color: rgb(111, 162, 255);")

        self.gridLayout.addWidget(self.new_btn, 11, 2, 1, 1)


        self.horizontalLayout_2.addWidget(self.frame_2)


        self.retranslateUi(students)

        QMetaObject.connectSlotsByName(students)
    # setupUi

    def retranslateUi(self, students):
        students.setWindowTitle(QCoreApplication.translate("students", u"Form", None))
        self.label_10.setText(QCoreApplication.translate("students", u"\u0627\u0644\u0625\u0633\u0645:", None))
        self.maximize.setText(QCoreApplication.translate("students", u"<", None))
        self.printing_btn.setText(QCoreApplication.translate("students", u"\u0637\u0628\u0627\u0639\u0629", None))
#if QT_CONFIG(shortcut)
        self.printing_btn.setShortcut(QCoreApplication.translate("students", u"Ctrl+P", None))
#endif // QT_CONFIG(shortcut)
        self.export_btn.setText(QCoreApplication.translate("students", u"excel", None))
#if QT_CONFIG(shortcut)
        self.export_btn.setShortcut(QCoreApplication.translate("students", u"Ctrl+E", None))
#endif // QT_CONFIG(shortcut)
        self.reset_btn.setText(QCoreApplication.translate("students", u"\u0625\u0639\u0627\u062f\u0629 \u0636\u0628\u0637", None))
#if QT_CONFIG(shortcut)
        self.reset_btn.setShortcut(QCoreApplication.translate("students", u"Esc", None))
#endif // QT_CONFIG(shortcut)
        self.search_btn.setText(QCoreApplication.translate("students", u"\u0628\u062d\u062b", None))
#if QT_CONFIG(shortcut)
        self.search_btn.setShortcut(QCoreApplication.translate("students", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.minimize.setText(QCoreApplication.translate("students", u">", None))
        self.groupBox.setTitle(QCoreApplication.translate("students", u"\u0645\u0633\u062c\u0644 \u0641\u064a \u0635\u0641", None))
        self.in_class.setItemText(0, QCoreApplication.translate("students", u"\u0646\u0639\u0645", None))
        self.in_class.setItemText(1, QCoreApplication.translate("students", u"\u0644\u0627", None))

        self.groupBox_2.setTitle(QCoreApplication.translate("students", u"\u0645\u0648\u0627\u0644\u064a\u062f \u0628\u064a\u0646", None))
        self.du.setDisplayFormat(QCoreApplication.translate("students", u"dd-MM-yyyy", None))
        self.to.setDisplayFormat(QCoreApplication.translate("students", u"dd-MM-yyyy", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("students", u"\u0645\u0639\u0641\u064a", None))
        self.excused_search.setItemText(0, QCoreApplication.translate("students", u"\u0646\u0639\u0645", None))
        self.excused_search.setItemText(1, QCoreApplication.translate("students", u"\u0644\u0627", None))

        self.groupBox_4.setTitle(QCoreApplication.translate("students", u"\u0641\u0627\u0639\u0644", None))
        self.activity_search.setItemText(0, QCoreApplication.translate("students", u"\u0641\u0627\u0639\u0644", None))
        self.activity_search.setItemText(1, QCoreApplication.translate("students", u"\u063a\u064a\u0631 \u0641\u0627\u0639\u0644", None))

        self.groupBox_5.setTitle(QCoreApplication.translate("students", u"\u0639\u062f\u062f \u0627\u0644\u062a\u0644\u0627\u0645\u064a\u0630", None))
        self.nb.setText("")
        self.label_7.setText(QCoreApplication.translate("students", u"\u0631\u0642\u0645 \u0627\u0644 \u0628 \u062a \u0648:", None))
        self.birthday.setDisplayFormat(QCoreApplication.translate("students", u"dd-MM-yyyy", None))
        self.gender.setItemText(0, QCoreApplication.translate("students", u"\u0630\u0643\u0631", None))
        self.gender.setItemText(1, QCoreApplication.translate("students", u"\u0623\u0646\u062b\u0649", None))

        self.label_6.setText(QCoreApplication.translate("students", u"\u0631\u0642\u0645 \u0627\u0644\u0647\u0627\u062a\u0641:", None))
        self.add_btn.setText(QCoreApplication.translate("students", u"\u0625\u0636\u0627\u0641\u0629", None))
        self.excused.setItemText(0, QCoreApplication.translate("students", u"\u0644\u0627", None))
        self.excused.setItemText(1, QCoreApplication.translate("students", u"\u0646\u0639\u0645", None))

        self.update_btn.setText(QCoreApplication.translate("students", u"\u062a\u063a\u064a\u064a\u0631", None))
        self.label_9.setText(QCoreApplication.translate("students", u"\u0627\u0644\u0646\u0634\u0627\u0637:", None))
        self.new_year.setText(QCoreApplication.translate("students", u"\u0633\u0646\u0629 \u0627\u0644\u062c\u062f\u064a\u062f\u0629", None))
        self.activity.setItemText(0, QCoreApplication.translate("students", u"\u0641\u0627\u0639\u0644", None))
        self.activity.setItemText(1, QCoreApplication.translate("students", u"\u063a\u064a\u0631 \u0641\u0627\u0639\u0644", None))

        self.label_3.setText(QCoreApplication.translate("students", u"\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0648\u0644\u0627\u062f\u0629:", None))
        self.label_12.setText(QCoreApplication.translate("students", u"\u0645\u0639\u0641\u0649:", None))
        self.delete_btn.setText(QCoreApplication.translate("students", u"\u062d\u0630\u0641", None))
        self.label_5.setText(QCoreApplication.translate("students", u"\u0625\u0633\u0645 \u0627\u0644\u0648\u0644\u064a:", None))
        self.label_2.setText(QCoreApplication.translate("students", u"\u0627\u0644\u0625\u0633\u0645:", None))
        self.date_inscrit.setDisplayFormat(QCoreApplication.translate("students", u"dd-MM-yyyy", None))
        self.label_11.setText(QCoreApplication.translate("students", u"\u062a \u0627\u0644\u062a\u0633\u062c\u064a\u0644:", None))
        self.label_16.setText(QCoreApplication.translate("students", u"\u0631\u0642\u0645 \u0627\u0644\u0647\u0627\u062a\u0641 2:", None))
        self.label_18.setText(QCoreApplication.translate("students", u"\u0627\u0644\u062c\u0646\u0633:", None))
        self.label_17.setText(QCoreApplication.translate("students", u"\u0645\u0644\u0627\u062d\u0638\u0629 \u0627\u0644\u062e\u0644\u0627\u0635:", None))
        self.new_btn.setText(QCoreApplication.translate("students", u"\u062c\u062f\u064a\u062f", None))
    # retranslateUi

