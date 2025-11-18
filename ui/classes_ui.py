# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'classes.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractSpinBox, QApplication, QComboBox,
    QDoubleSpinBox, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QTableView, QVBoxLayout,
    QWidget)

class Ui_classes_widget(object):
    def setupUi(self, classes_widget):
        if not classes_widget.objectName():
            classes_widget.setObjectName(u"classes_widget")
        classes_widget.setWindowModality(Qt.WindowModality.NonModal)
        classes_widget.resize(1107, 632)
        self.horizontalLayout = QHBoxLayout(classes_widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_3 = QFrame(classes_widget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.Box)
        self.frame_3.setFrameShadow(QFrame.Shadow.Plain)
        self.frame_3.setLineWidth(2)
        self.verticalLayout_2 = QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_2 = QFrame(self.frame_3)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.nb = QLabel(self.frame_2)
        self.nb.setObjectName(u"nb")
        self.nb.setMinimumSize(QSize(50, 0))
        self.nb.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setPointSize(15)
        self.nb.setFont(font)
        self.nb.setStyleSheet(u"border: 3px solid black; \n"
"border-radius: 15px")
        self.nb.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.nb)

        self.label_8 = QLabel(self.frame_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_8)

        self.horizontalSpacer_3 = QSpacerItem(276, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.teacher_search = QComboBox(self.frame_2)
        self.teacher_search.setObjectName(u"teacher_search")
        self.teacher_search.setMinimumSize(QSize(150, 30))
        self.teacher_search.setFont(font)
        self.teacher_search.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.teacher_search.setEditable(True)
        self.teacher_search.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        self.horizontalLayout_2.addWidget(self.teacher_search)

        self.label_9 = QLabel(self.frame_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_9)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.search = QLineEdit(self.frame_2)
        self.search.setObjectName(u"search")
        self.search.setMinimumSize(QSize(200, 30))
        self.search.setFont(font)
        self.search.setStyleSheet(u"border: 3px solid black;\n"
"border-left: none;\n"
"border-right: none;\n"
"border-top: none \n"
"")

        self.horizontalLayout_2.addWidget(self.search)

        self.label_7 = QLabel(self.frame_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_7)


        self.verticalLayout_2.addWidget(self.frame_2)

        self.class_table = QTableView(self.frame_3)
        self.class_table.setObjectName(u"class_table")
        self.class_table.setFont(font)
        self.class_table.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.class_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.class_table.setAlternatingRowColors(True)
        self.class_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.class_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.class_table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.class_table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.class_table.setShowGrid(False)
        self.class_table.horizontalHeader().setMinimumSectionSize(150)
        self.class_table.horizontalHeader().setDefaultSectionSize(150)
        self.class_table.verticalHeader().setCascadingSectionResizes(True)
        self.class_table.verticalHeader().setDefaultSectionSize(35)

        self.verticalLayout_2.addWidget(self.class_table)

        self.frame_7 = QFrame(self.frame_3)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)

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

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addWidget(self.frame_7)


        self.horizontalLayout.addWidget(self.frame_3)

        self.frame_4 = QFrame(classes_widget)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.Box)
        self.frame_4.setFrameShadow(QFrame.Shadow.Plain)
        self.frame_4.setLineWidth(2)
        self.verticalLayout_4 = QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.name = QLineEdit(self.frame_4)
        self.name.setObjectName(u"name")
        self.name.setFont(font)
        self.name.setStyleSheet(u"border: 3px solid black;\n"
"border-left: none;\n"
"border-right: none;\n"
"border-top: none \n"
"")

        self.horizontalLayout_3.addWidget(self.name)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.way = QComboBox(self.frame_4)
        self.way.setObjectName(u"way")
        self.way.setMinimumSize(QSize(0, 30))
        self.way.setFont(font)
        self.way.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.way.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        self.horizontalLayout_4.addWidget(self.way)

        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.horizontalLayout_4.addWidget(self.label_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.teacher = QComboBox(self.frame_4)
        self.teacher.setObjectName(u"teacher")
        self.teacher.setMinimumSize(QSize(0, 30))
        self.teacher.setFont(font)
        self.teacher.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.teacher.setEditable(True)
        self.teacher.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        self.horizontalLayout_6.addWidget(self.teacher)

        self.label_4 = QLabel(self.frame_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.horizontalLayout_6.addWidget(self.label_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.note = QLineEdit(self.frame_4)
        self.note.setObjectName(u"note")
        self.note.setFont(font)
        self.note.setStyleSheet(u"border: 3px solid black;\n"
"border-left: none;\n"
"border-right: none;\n"
"border-top: none \n"
"")

        self.horizontalLayout_7.addWidget(self.note)

        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_5)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.price = QLineEdit(self.frame_4)
        self.price.setObjectName(u"price")
        self.price.setFont(font)
        self.price.setStyleSheet(u"border: 3px solid black;\n"
"border-left: none;\n"
"border-right: none;\n"
"border-top: none \n"
"")

        self.horizontalLayout_8.addWidget(self.price)

        self.label_6 = QLabel(self.frame_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.horizontalLayout_8.addWidget(self.label_6)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.seance = QSpinBox(self.frame_4)
        self.seance.setObjectName(u"seance")
        self.seance.setFont(font)
        self.seance.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.seance.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.seance.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.seance.setMaximum(1111111111)

        self.horizontalLayout_12.addWidget(self.seance)

        self.label_11 = QLabel(self.frame_4)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.horizontalLayout_12.addWidget(self.label_11)


        self.verticalLayout_4.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.in_exchange = QComboBox(self.frame_4)
        self.in_exchange.addItem("")
        self.in_exchange.addItem("")
        self.in_exchange.setObjectName(u"in_exchange")
        self.in_exchange.setMinimumSize(QSize(0, 30))
        self.in_exchange.setFont(font)
        self.in_exchange.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.in_exchange.setEditable(False)
        self.in_exchange.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        self.horizontalLayout_13.addWidget(self.in_exchange)

        self.label_12 = QLabel(self.frame_4)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)

        self.horizontalLayout_13.addWidget(self.label_12)


        self.verticalLayout_4.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.teacher_price = QDoubleSpinBox(self.frame_4)
        self.teacher_price.setObjectName(u"teacher_price")
        self.teacher_price.setFont(font)
        self.teacher_price.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.teacher_price.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.teacher_price.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.teacher_price.setDecimals(2)
        self.teacher_price.setMaximum(11111111111111109993981897808543744.000000000000000)

        self.horizontalLayout_11.addWidget(self.teacher_price)

        self.label_10 = QLabel(self.frame_4)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.horizontalLayout_11.addWidget(self.label_10)


        self.verticalLayout_4.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.add_btn = QPushButton(self.frame_4)
        self.add_btn.setObjectName(u"add_btn")
        self.add_btn.setMinimumSize(QSize(120, 30))
        self.add_btn.setMaximumSize(QSize(120, 16777215))
        self.add_btn.setFont(font)
        self.add_btn.setStyleSheet(u"background-color: rgb(95, 199, 94);")

        self.horizontalLayout_9.addWidget(self.add_btn)

        self.new_btn = QPushButton(self.frame_4)
        self.new_btn.setObjectName(u"new_btn")
        self.new_btn.setMinimumSize(QSize(120, 30))
        self.new_btn.setMaximumSize(QSize(120, 16777215))
        self.new_btn.setFont(font)
        self.new_btn.setStyleSheet(u"background-color: rgb(111, 162, 255);")

        self.horizontalLayout_9.addWidget(self.new_btn)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.update_btn = QPushButton(self.frame_4)
        self.update_btn.setObjectName(u"update_btn")
        self.update_btn.setMinimumSize(QSize(120, 30))
        self.update_btn.setMaximumSize(QSize(120, 16777215))
        self.update_btn.setFont(font)
        self.update_btn.setStyleSheet(u"background-color: rgb(255, 160, 65);")

        self.horizontalLayout_10.addWidget(self.update_btn)

        self.delete_btn = QPushButton(self.frame_4)
        self.delete_btn.setObjectName(u"delete_btn")
        self.delete_btn.setMinimumSize(QSize(120, 30))
        self.delete_btn.setMaximumSize(QSize(120, 16777215))
        self.delete_btn.setFont(font)
        self.delete_btn.setStyleSheet(u"background-color: rgb(255, 74, 61);")

        self.horizontalLayout_10.addWidget(self.delete_btn)


        self.verticalLayout_4.addLayout(self.horizontalLayout_10)


        self.horizontalLayout.addWidget(self.frame_4)


        self.retranslateUi(classes_widget)

        QMetaObject.connectSlotsByName(classes_widget)
    # setupUi

    def retranslateUi(self, classes_widget):
        classes_widget.setWindowTitle(QCoreApplication.translate("classes_widget", u"Form", None))
        self.nb.setText("")
        self.label_8.setText(QCoreApplication.translate("classes_widget", u"\u0639\u062f\u062f \u0627\u0644\u0623\u0642\u0633\u0627\u0645:", None))
        self.label_9.setText(QCoreApplication.translate("classes_widget", u"\u0627\u0644\u0645\u0624\u062f\u0628:", None))
        self.label_7.setText(QCoreApplication.translate("classes_widget", u"\u0627\u0644\u0642\u0633\u0645:", None))
        self.printing_btn.setText(QCoreApplication.translate("classes_widget", u"\u0637\u0628\u0627\u0639\u0629", None))
#if QT_CONFIG(shortcut)
        self.printing_btn.setShortcut(QCoreApplication.translate("classes_widget", u"Ctrl+P", None))
#endif // QT_CONFIG(shortcut)
        self.export_btn.setText(QCoreApplication.translate("classes_widget", u"excel", None))
#if QT_CONFIG(shortcut)
        self.export_btn.setShortcut(QCoreApplication.translate("classes_widget", u"Ctrl+E", None))
#endif // QT_CONFIG(shortcut)
        self.label_2.setText(QCoreApplication.translate("classes_widget", u"\u0627\u0644\u0642\u0633\u0645:", None))
        self.label_3.setText(QCoreApplication.translate("classes_widget", u"\u0627\u0644\u0637\u0631\u064a\u0642\u0629/\u0627\u0644\u0645\u0627\u062f\u0629:", None))
        self.label_4.setText(QCoreApplication.translate("classes_widget", u"\u0627\u0644\u0645\u0624\u062f\u0628:", None))
        self.label_5.setText(QCoreApplication.translate("classes_widget", u"\u0645\u0644\u0627\u062d\u0638\u0629:", None))
        self.label_6.setText(QCoreApplication.translate("classes_widget", u"\u0627\u0644\u062b\u0645\u0646:", None))
        self.label_11.setText(QCoreApplication.translate("classes_widget", u"\u0639\u062f\u062f \u0627\u0644\u062d\u0635\u0635(\u0627\u0644\u0634\u0647\u0631):", None))
        self.in_exchange.setItemText(0, QCoreApplication.translate("classes_widget", u"\u0627\u0644\u062a\u0644\u0645\u064a\u0630", None))
        self.in_exchange.setItemText(1, QCoreApplication.translate("classes_widget", u"\u0627\u0644\u062d\u0635\u0629", None))

        self.label_12.setText(QCoreApplication.translate("classes_widget", u"\u0645\u0642\u0627\u0628\u0644:", None))
        self.label_10.setText(QCoreApplication.translate("classes_widget", u"\u062d\u0635\u0629 \u0627\u0644\u0623\u0633\u062a\u0627\u0630:", None))
        self.add_btn.setText(QCoreApplication.translate("classes_widget", u"\u0625\u0636\u0627\u0641\u0629", None))
        self.new_btn.setText(QCoreApplication.translate("classes_widget", u"\u062c\u062f\u064a\u062f", None))
        self.update_btn.setText(QCoreApplication.translate("classes_widget", u"\u062a\u063a\u064a\u064a\u0631", None))
        self.delete_btn.setText(QCoreApplication.translate("classes_widget", u"\u062d\u0630\u0641", None))
    # retranslateUi

