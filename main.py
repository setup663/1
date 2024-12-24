import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QMessageBox, QFormLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from design import MainWindowDesign, AddPositionWindowDesign, AddDepartmentWindowDesign, CalculateSalaryWindowDesign

# Создание базы данных SQLite и заполнение начальными данными
def create_database():
    conn = sqlite3.connect('staff.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            name TEXT,
            salary REAL,
            non_standard_bonus REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            hazard_bonus REAL
        )
    ''')

    # # Заполнение начальными данными
    # cursor.execute('INSERT OR IGNORE INTO positions (name, salary, non_standard_bonus) VALUES (?, ?, ?)',
    #                ('Менеджер', 50000, 0.1))
    # cursor.execute('INSERT OR IGNORE INTO positions (name, salary, non_standard_bonus) VALUES (?, ?, ?)',
    #                ('Разработчик', 70000, 0.15))
    # cursor.execute('INSERT OR IGNORE INTO departments (name, type, hazard_bonus) VALUES (?, ?, ?)',
    #                ('IT', 'Технический', 0.05))
    # cursor.execute('INSERT OR IGNORE INTO departments (name, type, hazard_bonus) VALUES (?, ?, ?)',
    #                ('HR', 'Административный', 0.02))

    conn.commit()
    conn.close()

# Функция для вычисления заработной платы
def calculate_salary(salary, hazard_bonus, non_standard_bonus):
    total_salary = salary * (1 + hazard_bonus + non_standard_bonus)
    tax = total_salary * 0.13
    net_salary = total_salary - tax
    return net_salary

# Основное окно
class MainWindow(QMainWindow, MainWindowDesign):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def open_add_position_window(self):
        self.add_position_window = AddPositionWindow(self)
        self.add_position_window.show()

    def open_add_department_window(self):
        self.add_department_window = AddDepartmentWindow(self)
        self.add_department_window.show()

    def open_calculate_salary_window(self):
        self.calculate_salary_window = CalculateSalaryWindow(self)
        self.calculate_salary_window.show()

# Окно для добавления должности
class AddPositionWindow(QWidget, AddPositionWindowDesign):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)

    def add_position(self):
        name = self.name_input.text()
        salary = float(self.salary_input.text())
        non_standard_bonus = float(self.non_standard_bonus_input.text())

        conn = sqlite3.connect('staff.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO positions (name, salary, non_standard_bonus) VALUES (?, ?, ?)',
                       (name, salary, non_standard_bonus))
        conn.commit()
        conn.close()

        QMessageBox.information(self, 'Успех', 'Должность добавлена успешно!')

# Окно для добавления подразделения
class AddDepartmentWindow(QWidget, AddDepartmentWindowDesign):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)

    def add_department(self):
        name = self.name_input.text()
        type_ = self.type_input.text()
        hazard_bonus = float(self.hazard_bonus_input.text())

        conn = sqlite3.connect('staff.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO departments (name, type, hazard_bonus) VALUES (?, ?, ?)',
                       (name, type_, hazard_bonus))
        conn.commit()
        conn.close()

        QMessageBox.information(self, 'Успех', 'Подразделение добавлено успешно!')

# Окно для расчета зарплаты
class CalculateSalaryWindow(QWidget, CalculateSalaryWindowDesign):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)

    def load_data(self):
        conn = sqlite3.connect('staff.db')
        cursor = conn.cursor()

        cursor.execute('SELECT name FROM positions')
        positions = cursor.fetchall()
        for position in positions:
            self.position_combo.addItem(position[0])

        cursor.execute('SELECT name FROM departments')
        departments = cursor.fetchall()
        for department in departments:
            self.department_combo.addItem(department[0])

        conn.close()

    def calculate_salary(self):
        position_name = self.position_combo.currentText()
        department_name = self.department_combo.currentText()

        conn = sqlite3.connect('staff.db')
        cursor = conn.cursor()

        cursor.execute('SELECT salary, non_standard_bonus FROM positions WHERE name = ?', (position_name,))
        position_data = cursor.fetchone()
        salary = position_data[0]
        non_standard_bonus = position_data[1]

        cursor.execute('SELECT hazard_bonus FROM departments WHERE name = ?', (department_name,))
        department_data = cursor.fetchone()
        hazard_bonus = department_data[0]

        conn.close()

        net_salary = calculate_salary(salary, hazard_bonus, non_standard_bonus)
        self.result_label.setText(f'Итоговая зарплата: {net_salary:.2f}')

# Создание базы данных
create_database()

# Запуск приложения
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
