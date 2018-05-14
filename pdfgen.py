from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QLineEdit, \
    QDateEdit
from PyQt5.QtCore import QRect, QDate
import datetime

class PrintingWindow(QMainWindow):
    def __init__(self):
        super().__init__()



        self.resize(400, 300)
        self.setObjectName('Создать PDF')

        self.title_lbl = QLabel(self)
        self.title_lbl.setText('Распечатать')
        self.title_lbl.setGeometry(QRect(10,10,300,20))

        self.start_date_lbl = QLabel(self)
        self.start_date_lbl.setText('Период, с')
        self.start_date_lbl.setGeometry(QRect(10, 40, 140, 20))

        self.start_date_picker = QDateEdit(self)
        self.start_date_picker.setGeometry(QRect(150, 40, 150, 20))
        self.start_date_picker.setDisplayFormat('yyyy-MM-dd')
        self.start_date_picker.setDate(QDate(2016, 1, 1))

        self.end_date_lbl = QLabel(self)
        self.end_date_lbl.setText('Период, по')
        self.end_date_lbl.setGeometry(QRect(10, 70, 140, 20))

        self.end_date_picker = QDateEdit(self)
        self.end_date_picker.setGeometry(QRect(150, 70, 150, 20))
        self.end_date_picker.setDisplayFormat('yyyy-MM-dd')
        self.end_date_picker.setDate(QDate(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day))

        self.main_dep = QLabel(self)
        self.main_dep.setText('Главное управление')
        self.main_dep.setGeometry(QRect(10, 100, 140, 20))

        self.main_dep = QLineEdit(self)
        self.main_dep.setGeometry(QRect(150, 100, 50, 20))

        self.print_btn = QPushButton('Экспорт PDF', self)
        self.print_btn.setGeometry(QRect(200, 260, 180, 20))
