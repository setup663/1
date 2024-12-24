from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QFormLayout, QWidget
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# Основное окно
class MainWindowDesign:
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle('Штатное расписание')
        MainWindow.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        MainWindow.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.title_label = QLabel('Штатное расписание')
        self.title_label.setFont(QFont('Arial', 20))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.add_position_button = QPushButton('Добавить должность')
        self.add_position_button.setStyleSheet('QPushButton {background-color: #4CAF50; color: white; padding: 10px; font-size: 16px;}')
        self.add_position_button.clicked.connect(MainWindow.open_add_position_window)
        self.layout.addWidget(self.add_position_button)

        self.add_department_button = QPushButton('Добавить подразделение')
        self.add_department_button.setStyleSheet('QPushButton {background-color: #4CAF50; color: white; padding: 10px; font-size: 16px;}')
        self.add_department_button.clicked.connect(MainWindow.open_add_department_window)
        self.layout.addWidget(self.add_department_button)

        self.calculate_salary_button = QPushButton('Рассчитать зарплату')
        self.calculate_salary_button.setStyleSheet('QPushButton {background-color: #4CAF50; color: white; padding: 10px; font-size: 16px;}')
        self.calculate_salary_button.clicked.connect(MainWindow.open_calculate_salary_window)
        self.layout.addWidget(self.calculate_salary_button)

# Окно для добавления должности
class AddPositionWindowDesign:
    def setupUi(self, AddPositionWindow):
        AddPositionWindow.setWindowTitle('Добавить должность')
        AddPositionWindow.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        AddPositionWindow.setLayout(self.layout)

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.name_input = QLineEdit()
        self.form_layout.addRow('Название должности:', self.name_input)

        self.salary_input = QLineEdit()
        self.form_layout.addRow('Оклад:', self.salary_input)

        self.non_standard_bonus_input = QLineEdit()
        self.form_layout.addRow('Процент надбавки за ненормированный рабочий день:', self.non_standard_bonus_input)

        self.add_button = QPushButton('Добавить')
        self.add_button.setStyleSheet('QPushButton {background-color: #4CAF50; color: white; padding: 10px; font-size: 16px;}')
        self.add_button.clicked.connect(AddPositionWindow.add_position)
        self.layout.addWidget(self.add_button)

        self.back_button = QPushButton('Назад')
        self.back_button.setStyleSheet('QPushButton {background-color: #f44336; color: white; padding: 10px; font-size: 16px;}')
        self.back_button.clicked.connect(AddPositionWindow.close)
        self.layout.addWidget(self.back_button)

# Окно для добавления подразделения
class AddDepartmentWindowDesign:
    def setupUi(self, AddDepartmentWindow):
        AddDepartmentWindow.setWindowTitle('Добавить подразделение')
        AddDepartmentWindow.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        AddDepartmentWindow.setLayout(self.layout)

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.name_input = QLineEdit()
        self.form_layout.addRow('Название подразделения:', self.name_input)

        self.type_input = QLineEdit()
        self.form_layout.addRow('Тип подразделения:', self.type_input)

        self.hazard_bonus_input = QLineEdit()
        self.form_layout.addRow('Процент надбавки за вредные условия труда:', self.hazard_bonus_input)

        self.add_button = QPushButton('Добавить')
        self.add_button.setStyleSheet('QPushButton {background-color: #4CAF50; color: white; padding: 10px; font-size: 16px;}')
        self.add_button.clicked.connect(AddDepartmentWindow.add_department)
        self.layout.addWidget(self.add_button)

        self.back_button = QPushButton('Назад')
        self.back_button.setStyleSheet('QPushButton {background-color: #f44336; color: white; padding: 10px; font-size: 16px;}')
        self.back_button.clicked.connect(AddDepartmentWindow.close)
        self.layout.addWidget(self.back_button)

# Окно для расчета зарплаты
class CalculateSalaryWindowDesign:
    def setupUi(self, CalculateSalaryWindow):
        CalculateSalaryWindow.setWindowTitle('Рассчитать зарплату')
        CalculateSalaryWindow.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        CalculateSalaryWindow.setLayout(self.layout)

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.position_combo = QComboBox()
        self.form_layout.addRow('Выберите должность:', self.position_combo)

        self.department_combo = QComboBox()
        self.form_layout.addRow('Выберите подразделение:', self.department_combo)

        self.calculate_button = QPushButton('Рассчитать')
        self.calculate_button.setStyleSheet('QPushButton {background-color: #4CAF50; color: white; padding: 10px; font-size: 16px;}')
        self.calculate_button.clicked.connect(CalculateSalaryWindow.calculate_salary)
        self.layout.addWidget(self.calculate_button)

        self.result_label = QLabel('')
        self.result_label.setFont(QFont('Arial', 16))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.result_label)

        self.back_button = QPushButton('Назад')
        self.back_button.setStyleSheet('QPushButton {background-color: #f44336; color: white; padding: 10px; font-size: 16px;}')
        self.back_button.clicked.connect(CalculateSalaryWindow.close)
        self.layout.addWidget(self.back_button)

        CalculateSalaryWindow.load_data()
