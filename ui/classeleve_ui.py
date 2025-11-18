# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'classeleve.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QTableView, QTextEdit, QVBoxLayout, QWidget)

class Ui_classeleve(object):
    def setupUi(self, classeleve):
        if not classeleve.objectName():
            classeleve.setObjectName(u"classeleve")
        classeleve.resize(1312, 716)
        self.verticalLayout = QVBoxLayout(classeleve)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.frame_2 = QFrame(classeleve)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.classeleve_stacked = QStackedWidget(self.frame_2)
        self.classeleve_stacked.setObjectName(u"classeleve_stacked")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.classeleve_stacked.sizePolicy().hasHeightForWidth())
        self.classeleve_stacked.setSizePolicy(sizePolicy1)
        self.classeleve_stacked.setFrameShape(QFrame.Shape.Box)
        self.classeleve_stacked.setFrameShadow(QFrame.Shadow.Plain)
        self.classeleve_stacked.setLineWidth(3)
        self.stackedWidget_4Page1 = QWidget()
        self.stackedWidget_4Page1.setObjectName(u"stackedWidget_4Page1")
        self.verticalLayout_2 = QVBoxLayout(self.stackedWidget_4Page1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_5 = QFrame(self.stackedWidget_4Page1)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.nb = QLabel(self.frame_5)
        self.nb.setObjectName(u"nb")
        self.nb.setMinimumSize(QSize(50, 0))
        self.nb.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setPointSize(15)
        self.nb.setFont(font)
        self.nb.setStyleSheet(u"border: 3px solid black; \n"
"border-radius: 15px")

        self.horizontalLayout_3.addWidget(self.nb)

        self.label_8 = QLabel(self.frame_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_8)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.classes = QComboBox(self.frame_5)
        self.classes.setObjectName(u"classes")
        self.classes.setMinimumSize(QSize(200, 0))
        self.classes.setFont(font)
        self.classes.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.classes.setEditable(True)

        self.horizontalLayout_3.addWidget(self.classes)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addWidget(self.frame_5)

        self.students = QTableView(self.stackedWidget_4Page1)
        self.students.setObjectName(u"students")
        self.students.setMinimumSize(QSize(500, 0))
        self.students.setMaximumSize(QSize(16777215, 16777215))
        self.students.setFont(font)
        self.students.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.students.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.students.setAlternatingRowColors(True)
        self.students.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.students.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.students.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.students.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.students.setShowGrid(False)
        self.students.horizontalHeader().setMinimumSectionSize(250)
        self.students.verticalHeader().setDefaultSectionSize(35)

        self.verticalLayout_2.addWidget(self.students)

        self.frame_7 = QFrame(self.stackedWidget_4Page1)
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

        self.clear_class = QPushButton(self.frame_7)
        self.clear_class.setObjectName(u"clear_class")
        self.clear_class.setMaximumSize(QSize(0, 16777215))

        self.horizontalLayout_5.addWidget(self.clear_class)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

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


        self.verticalLayout_2.addWidget(self.frame_7)

        self.classeleve_stacked.addWidget(self.stackedWidget_4Page1)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_4 = QVBoxLayout(self.page)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.frame_18 = QFrame(self.page)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.printing_plain = QTextEdit(self.frame_18)
        self.printing_plain.setObjectName(u"printing_plain")
        font1 = QFont()
        font1.setPointSize(12)
        self.printing_plain.setFont(font1)
        self.printing_plain.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.printing_plain.setReadOnly(True)

        self.horizontalLayout_15.addWidget(self.printing_plain)


        self.verticalLayout_4.addWidget(self.frame_18)

        self.frame_19 = QFrame(self.page)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_19)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_15)

        self.cancel = QPushButton(self.frame_19)
        self.cancel.setObjectName(u"cancel")
        self.cancel.setMinimumSize(QSize(150, 30))
        self.cancel.setFont(font)
        self.cancel.setStyleSheet(u"background-color: rgb(255, 93, 29);")

        self.horizontalLayout_14.addWidget(self.cancel)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_16)

        self.printing_unpayed = QPushButton(self.frame_19)
        self.printing_unpayed.setObjectName(u"printing_unpayed")
        self.printing_unpayed.setMinimumSize(QSize(150, 30))
        self.printing_unpayed.setFont(font)
        self.printing_unpayed.setStyleSheet(u"background-color: rgb(143, 255, 52);")

        self.horizontalLayout_14.addWidget(self.printing_unpayed)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_14)


        self.verticalLayout_4.addWidget(self.frame_19)

        self.classeleve_stacked.addWidget(self.page)

        self.horizontalLayout_2.addWidget(self.classeleve_stacked)

        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy2)
        self.frame_3.setMaximumSize(QSize(324, 16777215))
        self.frame_3.setFrameShape(QFrame.Shape.Box)
        self.frame_3.setFrameShadow(QFrame.Shadow.Plain)
        self.frame_3.setLineWidth(3)
        self.verticalLayout_3 = QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.student_search = QLineEdit(self.frame_3)
        self.student_search.setObjectName(u"student_search")
        self.student_search.setMinimumSize(QSize(0, 30))
        self.student_search.setFont(font)
        self.student_search.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.student_search.setStyleSheet(u"border: 3px solid black;\n"
"border-left: none;\n"
"border-right: none;\n"
"border-top: none \n"
"")

        self.verticalLayout_3.addWidget(self.student_search)

        self.student_search_list = QTableView(self.frame_3)
        self.student_search_list.setObjectName(u"student_search_list")
        self.student_search_list.setMinimumSize(QSize(300, 0))
        self.student_search_list.setFont(font)
        self.student_search_list.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.student_search_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.student_search_list.setAlternatingRowColors(True)
        self.student_search_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.student_search_list.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.student_search_list.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.student_search_list.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.student_search_list.setShowGrid(False)
        self.student_search_list.horizontalHeader().setMinimumSectionSize(150)

        self.verticalLayout_3.addWidget(self.student_search_list)


        self.horizontalLayout_2.addWidget(self.frame_3)


        self.verticalLayout.addWidget(self.frame_2)


        self.retranslateUi(classeleve)

        self.classeleve_stacked.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(classeleve)
    # setupUi

    def retranslateUi(self, classeleve):
        classeleve.setWindowTitle(QCoreApplication.translate("classeleve", u"Form", None))
        self.nb.setText("")
        self.label_8.setText(QCoreApplication.translate("classeleve", u"\u0639\u062f\u062f \u0627\u0644\u062a\u0644\u0627\u0645\u064a\u0630:", None))
        self.printing_btn.setText(QCoreApplication.translate("classeleve", u"\u0637\u0628\u0627\u0639\u0629", None))
#if QT_CONFIG(shortcut)
        self.printing_btn.setShortcut(QCoreApplication.translate("classeleve", u"Ctrl+P", None))
#endif // QT_CONFIG(shortcut)
        self.export_btn.setText(QCoreApplication.translate("classeleve", u"excel", None))
#if QT_CONFIG(shortcut)
        self.export_btn.setShortcut(QCoreApplication.translate("classeleve", u"Ctrl+E", None))
#endif // QT_CONFIG(shortcut)
        self.clear_class.setText(QCoreApplication.translate("classeleve", u"PushButton", None))
#if QT_CONFIG(shortcut)
        self.clear_class.setShortcut(QCoreApplication.translate("classeleve", u"Ctrl+L", None))
#endif // QT_CONFIG(shortcut)
        self.reset_btn.setText(QCoreApplication.translate("classeleve", u"\u0625\u0639\u0627\u062f\u0629 \u0636\u0628\u0637", None))
#if QT_CONFIG(shortcut)
        self.reset_btn.setShortcut(QCoreApplication.translate("classeleve", u"Esc", None))
#endif // QT_CONFIG(shortcut)
        self.search_btn.setText(QCoreApplication.translate("classeleve", u"\u0628\u062d\u062b", None))
#if QT_CONFIG(shortcut)
        self.search_btn.setShortcut(QCoreApplication.translate("classeleve", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.cancel.setText(QCoreApplication.translate("classeleve", u"\u0625\u0644\u063a\u0627\u0621", None))
#if QT_CONFIG(shortcut)
        self.cancel.setShortcut(QCoreApplication.translate("classeleve", u"Esc", None))
#endif // QT_CONFIG(shortcut)
        self.printing_unpayed.setText(QCoreApplication.translate("classeleve", u"\u0637\u0628\u0627\u0639\u0629", None))
    # retranslateUi

