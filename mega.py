from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QHeaderView
import sys
from AdminWindow import Ui_AdminWindow
from UserWindow import Ui_UserWindow
from AuthenticationWindow import Ui_AuthenticationWindow
from RegistrationWindow import Ui_RegistrationWindow
from add_changeWindow_user import Ui_Add_Change_window
from add_changeWindow_order import Ui_Add_Change_window2
from add_changeWindow_service import Ui_Add_Change_window3
from connetction import Data
from PyQt6.QtSql import QSqlTableModel

class Main_Programma(QMainWindow):
    def __init__(self):
        super().__init__()

        # окно аунтефикации
        self.Auth = QMainWindow()
        self.ui_Auth = Ui_AuthenticationWindow()
        self.ui_Auth.setupUi(self.Auth)

        self.ui_Auth.btn_enter_auth.clicked.connect(self.auth_process)
        self.ui_Auth.btn_exit_auth.clicked.connect(self.Exit_Auth)


        #окно регистрации
        self.Reg = QMainWindow()
        self.ui_Reg = Ui_RegistrationWindow()
        self.ui_Reg.setupUi(self.Reg)

        self.ui_Reg.btn_exit_reg.clicked.connect(self.Exit_Reg)
        self.ui_Reg.btn_enter_reg.clicked.connect(self.reg_process)
        #окно пользователя
        self.User = QMainWindow()
        self.ui_User = Ui_UserWindow()
        self.ui_User.setupUi(self.User)

        self.ui_User.btn_exit_user.clicked.connect(self.Exit_User)
        self.ui_User.btn_save.clicked.connect(self.user_process)

        # окно админа
        self.Admin = QMainWindow()
        self.ui_Admin = Ui_AdminWindow()
        self.ui_Admin.setupUi(self.Admin)
        self.conn = Data()
        self.view_data1()
        self.view_data2()
        self.view_data3()

        self.ui_Admin.graphWidget.setLabel('left', "<span style=\"color:white;font-size:13px\">-----------цена-----------</span>")
        self.ui_Admin.graphWidget.setLabel('bottom', "<span style=\"color:white;font-size:13px\">------колличество заказов------</span>")

        self.ui_Admin.btn_exit_admin.clicked.connect(self.Exit_Admin)
        self.ui_Admin.btn_select_date.clicked.connect(self.info_price)

        self.ui_Admin.btn_add1.clicked.connect(self.open_add_change1)
        self.ui_Admin.btn_change1.clicked.connect(self.open_add_change1)
        self.ui_Admin.btn_delete1.clicked.connect(self.delete_query1)

        self.ui_Admin.btn_add2.clicked.connect(self.open_add_change2)
        self.ui_Admin.btn_change2.clicked.connect(self.open_add_change2)
        self.ui_Admin.btn_delete2.clicked.connect(self.delete_query2)

        self.ui_Admin.btn_add3.clicked.connect(self.open_add_change3)
        self.ui_Admin.btn_change3.clicked.connect(self.open_add_change3)
        self.ui_Admin.btn_delete3.clicked.connect(self.delete_query3)

    def info_price(self):
        info_date = str(self.ui_Admin.dateEdit_admin.text())

        con_info = self.conn.info(info_date)
        self.ui_Admin.graphWidget.plot(con_info[0], con_info[1])

    def view_data1(self):
        self.model = QSqlTableModel(self)
        self.model.setTable("пользователи")
        horizontal_header = self.ui_Admin.tableView_1.horizontalHeader()
        horizontal_header = self.ui_Admin.tableView_1.horizontalHeader()
        horizontal_header.orientation = QtCore.Qt.Orientation.Vertical
        horizontal_header.setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        horizontal_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.model.select()
        self.ui_Admin.tableView_1.setModel(self.model)



    def view_data2(self):
        self.model = QSqlTableModel(self)
        self.model.setTable("заказы")
        self.model.select()
        self.ui_Admin.tableView_2.setModel(self.model)

    def view_data3(self):
        self.model = QSqlTableModel(self)
        self.model.setTable("услуги")
        self.model.select()
        self.ui_Admin.tableView_3.setModel(self.model)


    def Exit_Auth(self):
        self.Auth.close()
        self.Reg.show()


    def Exit_Reg(self):
        self.Reg.close()
        self.Auth.show()


    def Exit_Admin(self):
        self.Admin.close()
        self.Auth.show()


    def Exit_User(self):
        self.User.close()
        self.Auth.show()

    def auth_process(self):
        login = self.ui_Auth.edit_login_auth.text()
        password = self.ui_Auth.edit_password_auth.text()
        role = self.conn.get_user(login, password)
        self.ui_User.label_Firstname_edit.setText(role.value(1))
        self.ui_User.label_Lastname_edit.setText(role.value(2))
        self.ui_User.label_age_edit.setText(str(role.value(5)))
        self.ui_User.label_phone_edit.setText(role.value(6))

        if role:
            super_user = role.value(7)

            if super_user == 'yes':
                self.Admin.show()
                self.Auth.close()
            elif super_user == 'no':
                self.User.show()
                self.Auth.close()
        return role.value(0)


    def reg_process(self):
        login = self.ui_Reg.edit_login_reg.text()
        password = self.ui_Reg.edit_password_reg.text()
        if not login or not password:
            return
        user_query = self.conn.get_user(login, password)
        if user_query:
            return
        self.conn.add_user(login, password)
        self.Auth.show()
        self.Reg.close()


    def user_process(self):
        id_user = self.auth_process()
        firstname = self.ui_User.edit_Firstname.toPlainText()
        lastname = self.ui_User.edit_Lastname.toPlainText()
        age = int(self.ui_User.edit_age.toPlainText())
        number_phone = self.ui_User.edit_phone.toPlainText()
        mark = self.ui_User.edit_mark.toPlainText()
        description = self.ui_User.edit_description.toPlainText()
        date = self.ui_User.dateEdit_user.text()

        self.conn.add_data_user(firstname, lastname, age, number_phone, id_user)
        self.conn.add_data_order(id_user, mark, description, date)
        self.view_data1()

    def open_add_change1(self):
        self.add_change1 = QDialog()
        self.ui_add_change1 = Ui_Add_Change_window()
        self.ui_add_change1.setupUi(self.add_change1)
        self.add_change1.show()
        sender = self.sender()
        if sender.text() == "добавить":
            self.ui_add_change1.btn_add_diag.clicked.connect(self.add_query1)
        else:
            self.ui_add_change1.btn_add_diag.clicked.connect(self.change_query1)

    def open_add_change2(self):
        self.add_change2 = QDialog()
        self.ui_add_change2 = Ui_Add_Change_window2()
        self.ui_add_change2.setupUi(self.add_change2)
        self.add_change2.show()
        sender = self.sender()
        if sender.text() == "добавить":
            self.ui_add_change2.btn_add_diag.clicked.connect(self.add_query2)
        else:
            self.ui_add_change2.btn_add_diag.clicked.connect(self.change_query2)

    def open_add_change3(self):
        self.add_change3 = QDialog()
        self.ui_add_change3 = Ui_Add_Change_window3()
        self.ui_add_change3.setupUi(self.add_change3)
        self.add_change3.show()
        sender = self.sender()
        if sender.text() == "добавить":
            self.ui_add_change3.btn_add_diag.clicked.connect(self.add_query3)
        else:
            self.ui_add_change3.btn_add_diag.clicked.connect(self.change_query3)


    def add_query1(self):
        firstname = self.ui_add_change1.edit_Firstname_diag.toPlainText()
        lastname = self.ui_add_change1.edit_Lastname_diag.toPlainText()
        login = self.ui_add_change1.edit_Login_diag.toPlainText()
        password = self.ui_add_change1.edit_Password_diag.toPlainText()
        age = self.ui_add_change1.edit_Age_diag.toPlainText()
        number_phone = self.ui_add_change1.edit_number_phone_diag.toPlainText()
        admin = self.ui_add_change1.edit_Admin_diag.toPlainText()
        self.conn.add_new1(firstname, lastname, login, password, age, number_phone, admin)
        self.view_data1()
        self.add_change1.close()

    def add_query2(self):
        id_user = int(self.ui_add_change2.edit_id_user_diag.toPlainText())
        id_service = int(self.ui_add_change2.edit_id_service_diag.toPlainText())
        mark = self.ui_add_change2.edit_Mark_diag.toPlainText()
        description = self.ui_add_change2.edit_Description_diag.toPlainText()
        date = self.ui_add_change2.edit_Date_diag.toPlainText()

        self.conn.add_new2(id_user, id_service, mark, description, date)
        self.view_data2()
        self.add_change2.close()


    def add_query3(self):
        name = self.ui_add_change3.edit_name_diag.toPlainText()
        price = self.ui_add_change3.edit_price_diag.toPlainText()

        self.conn.add_new3(name, price)
        self.view_data3()
        self.add_change3.close()


    def change_query1(self):
        index = self.ui_Admin.tableView_1.selectedIndexes()[0]
        id = str(self.ui_Admin.tableView_1.model().data(index))
        firstname = self.ui_add_change1.edit_Firstname_diag.toPlainText()
        lastname = self.ui_add_change1.edit_Lastname_diag.toPlainText()
        login = self.ui_add_change1.edit_Login_diag.toPlainText()
        password = self.ui_add_change1.edit_Password_diag.toPlainText()
        age = self.ui_add_change1.edit_Age_diag.toPlainText()
        number_phone = self.ui_add_change1.edit_number_phone_diag.toPlainText()
        admin = self.ui_add_change1.edit_Admin_diag.toPlainText()
        self.conn.change1(firstname, lastname, login, password, age, number_phone, admin, id)

        self.view_data1()
        self.add_change1.close()

    def change_query2(self):
        index = self.ui_Admin.tableView_2.selectedIndexes()[0]
        id = str(self.ui_Admin.tableView_2.model().data(index))
        id_user = int(self.ui_add_change2.edit_id_user_diag.toPlainText())
        id_service = int(self.ui_add_change2.edit_id_service_diag.toPlainText())
        mark = self.ui_add_change2.edit_Mark_diag.toPlainText()
        description = self.ui_add_change2.edit_Description_diag.toPlainText()
        date = self.ui_add_change2.edit_Date_diag.toPlainText()
        self.conn.change2(id_user, id_service, mark, description, date, id)

        self.view_data2()
        self.add_change2.close()

    def change_query3(self):
        index = self.ui_Admin.tableView_3.selectedIndexes()[0]
        id = str(self.ui_Admin.tableView_3.model().data(index))
        name = self.ui_add_change3.edit_name_diag.toPlainText()
        price = self.ui_add_change3.edit_price_diag.toPlainText()
        self.conn.change3(name, price, id)

        self.view_data3()
        self.add_change3.close()

    def delete_query1(self):
        index = self.ui_Admin.tableView_1.selectedIndexes()[0]
        id = str(self.ui_Admin.tableView_1.model().data(index))
        self.conn.delete1(id)
        self.view_data1()

    def delete_query2(self):
        index = self.ui_Admin.tableView_2.selectedIndexes()[0]
        id = str(self.ui_Admin.tableView_2.model().data(index))
        self.conn.delete2(id)
        self.view_data2()

    def delete_query3(self):
        index = self.ui_Admin.tableView_3.selectedIndexes()[0]
        id = str(self.ui_Admin.tableView_3.model().data(index))
        self.conn.delete3(id)
        self.view_data3()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    programma = Main_Programma()

    programma.Auth.show()
    sys.exit(app.exec())