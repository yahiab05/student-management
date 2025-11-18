from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from .help import HelpLogic
from .models import Settings, OutMoney, Entery, Classes
from .database import SessionLocal
from sqlalchemy.exc import IntegrityError
from os import path


class SettingsLogic(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        BASE_DIR = path.dirname(path.abspath(__file__))
        loadUi(path.join(BASE_DIR, "..", "ui", "settings.ui"), self)

        self.identifier = 0

        self.setup()
        self.out_show()
        self.entery_show()
        self.way_show()
        self.payment_show()
        self.fournisseur_show()

    def setup(self):
        self.out_setup()
        self.entery_setup()
        self.way_setup()
        self.payment_setup()
        self.fournisseur_setup()

    """Out section"""
    def out_setup(self):
        self.out_new_btn.clicked.connect(self.out_reset)
        self.out_add_btn.clicked.connect(lambda: self.out_control("add"))
        self.out_update_btn.clicked.connect(lambda: self.out_control("update"))
        self.out_delete_btn.clicked.connect(self.out_delete)
        self.out_list.itemDoubleClicked.connect(self.out_select_row)
        self.out_ent.textChanged.connect(lambda: self.out_show(self.out_ent.text()))

    def out_control(self, action):
        name = self.out_ent.text()
        code = self.out_code.text()
        if name == "":
            HelpLogic.error("الرجاء إضافة نوعية دخل")
        elif code == "0":
            HelpLogic.error("الرجاء التثبة من الرمز")
        else:
            if action == "add":
                self.out_add(name, code)
            else:
                self.out_update(name, code)

    def out_add(self, name, code):
        session = SessionLocal()

        try:
            new_out = Settings(out_money=name, out_code=code)
            session.add(new_out)
            session.commit()
        except IntegrityError:
            session.rollback()
            HelpLogic.error("هذا النوع من المصاريف موجود.")
        finally:
            session.close()
            self.out_reset()

    def out_update(self, name, code):
        session = SessionLocal()

        out = session.query(Settings).filter(Settings.id == self.identifier).first()

        try:
            if out is not None:
                out.out_money = name
                out.out_code = code
                session.commit()
            else:
                HelpLogic.error("هذا النوع من المصاريف غير موجود.")
        except IntegrityError:
            session.rollback()
            HelpLogic.error("هذا النوع من المصاريف موجود.")
        finally:
            session.close()
            self.out_reset()
        
        self.identifier = 0

    def out_delete(self):
        code = int(self.out_ent.text())
        if self.out_check_used(code):
            HelpLogic.error("لا يمكن الحذف لأنه يتم إستعماله")
        else:
            session = SessionLocal()

            if out:
                out = session.query(Settings).filter(Settings.out_code == code).first()
                session.delete(out)
                session.commit()
            else:
                HelpLogic.error("هذا النوع من المصاريف غير موجود.")
        self.out_reset()
        self.identifier = 0

    def out_check_used(self, code):
        session = SessionLocal()

        data = session.query(OutMoney).filter(OutMoney.code == code).first()

        session.close()
        if data is None:
            return False
        else:
            return True

    def out_reset(self):
        self.out_code.setValue(0)
        self.out_ent.setText("")

        self.out_show()

    def out_select_row(self):
        row = self.out_list.currentRow()
        self.identifier = int(self.out_list.item(row, 0).text())
        self.out_ent.setText(self.out_list.item(row, 1).text())
        self.out_code.setValue(int(self.out_list.item(row, 2).text()))

    def out_show(self, name=None):
        session = SessionLocal()

        if name is None:
            data = session.query(Settings).with_entities(Settings.id, 
                    Settings.out_money, Settings.out_code).filter(
                        Settings.out_money != None).all()
        else:
            data = session.query(Settings).with_entities(Settings.id, 
                    Settings.out_money, Settings.out_code).filter(
                        Settings.out_money.ilike(f"%{name}%")).all()
        self.out_list.setRowCount(len(data))
        if len(data) > 0:
            for i, class_obj in enumerate(data):
                self.out_list.setItem(i, 0, QTableWidgetItem(str(class_obj.id)))
                self.out_list.setItem(i, 1, QTableWidgetItem(str(class_obj.out_money)))
                self.out_list.setItem(i, 2, QTableWidgetItem(str(class_obj.out_code)))

        self.out_nb.setText(str(len(data)))

        session.close()


    """Entery section"""

    def entery_setup(self):
        self.entery_new_btn.clicked.connect(self.entery_reset)
        self.entery_add_btn.clicked.connect(lambda: self.entery_control("add"))
        self.entery_update_btn.clicked.connect(lambda: self.entery_control("update"))
        self.entery_delete_btn.clicked.connect(self.entery_delete)
        self.entery_list.itemDoubleClicked.connect(self.entery_select_row)
        self.entery_ent.textChanged.connect(lambda: self.entery_show(self.entery_ent.text()))

    def entery_control(self, action):
        name = self.entery_ent.text()
        code = self.entery_code.text()
        if name == "":
            HelpLogic.error("الرجاء إضافة نوعية دخل")
        elif code == "0":
            HelpLogic.error("الرجاء التثبة من الرمز")
        else:
            if action == "add":
                self.entery_add(name, code)
            else:
                self.entery_update(name, code)

    def entery_add(self, name, code):
        session = SessionLocal()

        try:
            new_entery = Settings(entery=name, entery_code=code)
            session.add(new_entery)
            session.commit()
        except IntegrityError:
            session.rollback()
            HelpLogic.error("هذا النوع موجود.")
        finally:
            session.close()
            self.entery_reset()

    def entery_update(self, name, code):
        session = SessionLocal()

        entery = session.query(Settings).filter(Settings.id == self.identifier).first()

        try:
            if entery is not None:
                entery.entery = name
                entery.entery_code = code
                session.commit()
            else:
                HelpLogic.error("هذا النوع غير موجود.")
        except IntegrityError:
            session.rollback()
            HelpLogic.error("هذا النوع من المصاريف موجود.")
        finally:
            session.close()
            self.entery_reset()
        
        self.identifier = 0

    def entery_delete(self):
        code = int(self.out_ent.text())
        if self.entery_check_used(code):
            HelpLogic.error("لا يمكن الحذف لأنه يتم إستعماله")
        else:
            session = SessionLocal()
            entery = session.query(Settings).filter(Settings.entery_code == code).first()

            if entery:
                session.delete(entery)
                session.commit()
            else:
                HelpLogic.error("هذا النوع من المصاريف غير موجود.")
            session.close()
        self.entery_reset()
        self.identifier = 0

    def entery_check_used(self, code):
        session = SessionLocal()

        data = session.query(Entery).filter(Entery.code == code).first()

        session.close()
        if data is None:
            return False
        else:
            return True

    def entery_reset(self):
        self.entery_code.setValue(0) 
        self.entery_ent.setText("")

        self.entery_show()

    def entery_select_row(self):
        if int(self.entery_list.item(row, 2).text()) != 13:
            row = self.entery_list.currentRow()
            self.identifier = int(self.entery_list.item(row, 0).text())
            self.entery_ent.setText(self.entery_list.item(row, 1).text())
            self.entery_code.setValue((int(self.entery_list.item(row, 2).text())))
        else:
            HelpLogic.error("لا يمكن التحديث")

    def entery_show(self, name=None):
        session = SessionLocal()

        if name is None:
            data = session.query(Settings).with_entities(Settings.id, 
                    Settings.entery, Settings.entery_code).filter(
                        Settings.entery != None).all()
        else:
            data = session.query(Settings).with_entities(Settings.id, 
                    Settings.entery, Settings.entery_code).filter(
                        Settings.entery.ilike(f"%{name}%")).all()
            
        if len(data) > 0:
            self.entery_list.setRowCount(len(data))
            for i, class_obj in enumerate(data):
                self.entery_list.setItem(i, 0, QTableWidgetItem(str(class_obj.id)))
                self.entery_list.setItem(i, 1, QTableWidgetItem(str(class_obj.entery)))
                self.entery_list.setItem(i, 2, QTableWidgetItem(str(class_obj.entery_code)))
        else:
            self.entery_list.setRowCount(0)

        self.entery_nb.setText(str(len(data)))

        session.close()


    """way of teaching section"""

    def way_setup(self):
        self.way_new_btn.clicked.connect(self.way_reset)
        self.way_add_btn.clicked.connect(lambda: self.way_control("add"))
        self.way_update_btn.clicked.connect(lambda: self.way_control("update"))
        self.way_delete_btn.clicked.connect(self.way_delete)
        self.way_list.itemDoubleClicked.connect(self.way_select_row)
        self.way_ent.textChanged.connect(lambda: self.way_show(self.way_ent.text()))

    def way_control(self, action):
        name = self.way_ent.text()
        if name != "":
            if action == "add":
                self.way_add(name)
            else:
                self.way_update(name)
        else:
            HelpLogic.error("الرجاء إضافة إسم")

    def way_add(self, name):
        session = SessionLocal()

        try:
            new_way = Settings(way_teaching=name)
            session.add(new_way)
            session.commit()
        except IntegrityError:
            session.rollback()
            HelpLogic.error("هذه الطريقة موجودة")
        finally:
            session.close()
            self.way_reset()

    def way_update(self, name):
        session = SessionLocal()

        way = session.query(Settings).filter(Settings.way_teaching == name).first()

        if way is not None:
            try:
                way.way_teaching = name
                session.commit()
            except IntegrityError:
                session.rollback()
                HelpLogic.error("هذه الطريقة موجودة")
            finally:
                session.close()
                self.way_reset()
        else:
            HelpLogic.error("هذه الطريقة غير موجودة")

    def way_delete(self):
        name = self.way_ent.text()
        session = SessionLocal()

        way = session.query(Settings).filter(Settings.way_teaching == name).first()

        if self.way_check_used(name):
            HelpLogic.error("لا يمكن الحذف لأنه يتم إستعماله")
        else:
            if way is not None:
                session.delete(way)
                session.commit()
            else:
                HelpLogic.error("هذه الطريقة غير موجودة")
        session.close()
        self.way_reset()

    def way_check_used(self, way):
        session = SessionLocal()

        data = session.query(Classes).filter(Classes.way == way).first()

        session.close()
        if data is None:
            return False
        else:
            return True

    def way_reset(self):
        self.way_ent.setText("")

        self.way_show()  

    def way_select_row(self):
        way = self.way_list.currentItem().text()
        self.way_ent.setText(way)

    def way_show(self, name=None):
        session = SessionLocal()

        if name is None:
            data = session.query(Settings).with_entities(
                Settings.way_teaching).filter(
                    Settings.way_teaching != None).all()
        else:
            data = session.query(Settings).with_entities(
                Settings.way_teaching).filter(
                    Settings.way_teaching.ilike(f"%{name}%")).all()
            
        self.way_list.clear()

        if len(data) > 0:
            for item in data:
                self.way_list.addItem(item[0])

        self.way_nb.setText(str(len(data)))

        session.close()

    """way of payment section"""

    def payment_setup(self):
        self.moyen_payment_new_btn.clicked.connect(self.payment_reset)
        self.moyen_payment_add_btn.clicked.connect(lambda: self.payment_control("add"))
        self.moyen_payment_update_btn.clicked.connect(lambda: self.payment_control("update"))
        self.moyen_payment_delete_btn.clicked.connect(self.payment_delete)
        self.moyen_payment_list.itemDoubleClicked.connect(self.payment_select_row)
        self.moyen_payment_ent.textChanged.connect(lambda: self.payment_show(self.moyen_payment_ent.text()))

    def payment_control(self, action):
        name = self.moyen_payment_ent.text()
        if name != "":
            if action == "add":
                self.payment_add(name)
            else:
                self.payment_add(name)
        else:
            HelpLogic.error("الرجاء إضافة إسم")

    def payment_add(self, name):
        session = SessionLocal()

        try:
            new_way = Settings(way_payment=name)
            session.add(new_way)
            session.commit()
        except IntegrityError:
            session.rollback()
            HelpLogic.error("هذه الطريقة موجودة")
        finally:
            session.close()
            self.payment_reset()

    def payment_update(self, name):
        session = SessionLocal()

        way = session.query(Settings).filter(Settings.way_payment == name).first()

        if way is not None:
            try:
                way.way_payment = name
                session.commit()
            except IntegrityError:
                session.rollback()
                HelpLogic.error("هذه الطريقة موجودة")
            finally:
                session.close()
                self.payment_reset()
        else:
            HelpLogic.error("هذه الطريقة غير موجودة")

    def payment_delete(self):
        name = self.moyen_payment_ent.text()
        session = SessionLocal()

        way = session.query(Settings).filter(Settings.way_payment == name).first()

        if self.payment_chesck_used(name):
            HelpLogic.error("لا يمكن الحذف لأنه يتم إستعماله")
        else:
            if way is not None:
                session.delete(way)
                session.commit()
            else:
                HelpLogic.error("هذه الطريقة غير موجودة")
        session.close()
        self.payment_reset()

    def payment_chesck_used(self, name):
        session = SessionLocal()

        data1 = session.query(Entery).filter(Entery.way == name).first()
        data2 = session.query(OutMoney).filter(OutMoney.way == name).first()
        
        session.close()
        if data1 is None and data2 is None:
            return False
        return True

    def payment_reset(self):
        self.moyen_payment_ent.setText("")

        self.payment_show()

    def payment_select_row(self):
        way = self.moyen_payment_list.currentItem().text()
        if way == "صك":
            HelpLogic.error("لا يمكنك اختيار صك")
            return
        self.moyen_payment_ent.setText(way)

    def payment_show(self, name=None):
        session = SessionLocal()

        if name is None:
            data = session.query(Settings).with_entities(
                Settings.way_payment).filter(
                    Settings.way_payment != None).all()
        else:
            data = session.query(Settings).with_entities(
                Settings.way_payment).filter(
                    Settings.way_payment.ilike(f"%{name}%")).all()

        self.moyen_payment_list.clear()
        if len(data) > 0:
            for item in data:
                self.moyen_payment_list.addItem(item[0])

        self.moyen_payment_nb.setText(str(len(data)))

        session.close()

    """fournisseur section"""

    def fournisseur_setup(self):
        self.fr_new_btn.clicked.connect(self.fournisseur_reset)
        self.fr_add_btn.clicked.connect(lambda: self.fournisseur_control("add"))
        self.fr_update_btn.clicked.connect(lambda: self.fournisseur_control("update"))
        self.fr_delete_btn.clicked.connect(self.fournisseur_delete)
        self.fr_list.itemDoubleClicked.connect(self.fournisseur_select_row)
        self.fr_ent.textChanged.connect(lambda: self.fournisseur_show(self.fr_ent.text()))

    def fournisseur_control(self, action):
        name = self.fr_ent.text()
        if name != "":
            if action == "add":
                self.fournisseur_add(name)
            else:
                self.fournisseur_update(name)
        else:
            HelpLogic.error("الرجاء إضافة إسم")

    def fournisseur_add(self, name):
        session = SessionLocal()

        try:
            new_way = Settings(fr=name)
            session.add(new_way)
            session.commit()
        except IntegrityError:
            session.rollback()
            HelpLogic.error("هذا المورد موجود.")
        finally:
            session.close()
            self.fournisseur_reset()

    def fournisseur_update(self, name):
        session = SessionLocal()

        fr = session.query(Settings).filter(Settings.fr == name).first()

        if fr is not None:
            try:
                fr.fr = name
                session.commit()
            except IntegrityError:
                session.rollback()
                HelpLogic.error("هذا المورد موجود.")
            finally:
                session.close()
                self.fournisseur_reset()
        else:
            HelpLogic.error("هذا المورد غير موجود.")
            session.close()

    def fournisseur_delete(self):
        name = self.fr_ent.text()
        session = SessionLocal()

        fr = session.query(Settings).filter(Settings.fr == name).first()

        if self.fournisseur_check_used(name):
            HelpLogic.error("لا يمكن الحذف لأنه يتم إستعماله")
        else:
            if fr is not None:
                session.delete(fr)
                session.commit()
            else:
                HelpLogic.error("هذا المورد غير موجود.")
        session.close()
        self.fournisseur_reset()

    def fournisseur_check_used(self, name):
        session = SessionLocal()
        print(name)

        query = session.query(OutMoney).filter(OutMoney.name == name).first()
        print(query)

        session.close()

        if query is None:
            return False
        return True

    def fournisseur_reset(self):
        self.fr_ent.setText("")

        self.fournisseur_show()

    def fournisseur_select_row(self):
        fr = self.fr_list.currentItem().text()
        self.fr_ent.setText(fr)

    def fournisseur_show(self, name=None):
        session = SessionLocal()

        if name is None:
            data = session.query(Settings).with_entities(Settings.fr).filter(
                Settings.fr != None).all()
        else:
            data = session.query(Settings).with_entities(Settings.fr).filter(
                Settings.fr.ilike(f"%{name}%")).all()

        self.fr_list.clear()

        if len(data) > 0:
            for item in data:
                self.fr_list.addItem(item[0])

        self.fr_nb.setText(str(len(data)))

        session.close()
