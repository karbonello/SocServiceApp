from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QWidget, \
    QGroupBox, QTableView, QComboBox
from PyQt5.QtGui import QFont, QWindow, QImage, QPalette, QBrush
from PyQt5.QtCore import QCoreApplication, QRect, QMetaObject, QSize

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        offset_top = 50
        first_row_box_height = 250
        main_height = 650
        main_width = 1050

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(main_width, main_height)
        MainWindow.setMaximumSize(main_width, main_height)
        MainWindow.setMinimumSize(main_width, main_height)

        oImage = QImage("static/images/wallpaper.jpg")
        sImage = oImage.scaled(QSize(main_width, main_height))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))

        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName("centralwidget")
        self.central_widget.setStyleSheet('background')
        #self.central_widget.setPalette(central_widget_palette)
        MainWindow.setPalette(palette)

        title_font = QFont("Calibri", 25, QFont.Bold)
        self.title_label = QLabel(self.central_widget)
        self.title_label.setText('Social Service')
        self.title_label.setGeometry(QRect(20, 6, 300, 40))
        self.title_label.setFont(title_font)

        self.qbtn = QPushButton('Выход', self.central_widget)
        self.qbtn.clicked.connect(QCoreApplication.instance().quit)
        self.qbtn.move(950, 615)

        self.input_box = QGroupBox(self.central_widget)
        self.input_box.setGeometry(QRect(10, offset_top, main_width - 20, first_row_box_height))

        self.db_info_box = QGroupBox(self.central_widget)
        self.db_info_box.setGeometry(QRect(10, offset_top + first_row_box_height + 10,
                                           main_width - 20, 300)
                                     )

        #self.results_box = QGroupBox(self.central_widget)
        #self.results_box.setGeometry(QRect(320, first_row_box_height + offset_top + 35,
        #                                   MainWindow.width() - 330, 180)
        #                             )

        # Заполняем первый бокс
        self.input_box_label = QLabel(self.input_box)
        self.input_box_label.setText('Данные для коэффициентов')
        self.input_box_label.setGeometry(QRect(10, 10, 300, 20))
        self.input_box_label.setFont(QFont('Calibri', 14, QFont.Bold))

        self.village_number_lbl = QLabel(self.input_box)
        self.village_number_lbl.setGeometry(QRect(10, offset_top, 411, 20))
        self.village_number_lbl.setText('Кол-во подопечных в сёлах')

        self.village_number_edit = QLineEdit(self.input_box)
        self.village_number_edit.setGeometry(QRect(220, offset_top, 100, 20))

        self.city_number_lbl = QLabel(self.input_box)
        self.city_number_lbl.setGeometry(QRect(10, offset_top + 30, 411, 20))
        self.city_number_lbl.setText('Кол-во подопечных в городах')

        self.city_number_edit = QLineEdit(self.input_box)
        self.city_number_edit.setGeometry(QRect(220, offset_top + 30, 100, 20))

        self.base_lbl = QLabel(self.input_box)
        self.base_lbl.setGeometry(QRect(10, offset_top + 60, 411, 20))
        self.base_lbl.setText('Базовые нормативные затраты')

        self.base_edit = QLineEdit(self.input_box)
        self.base_edit.setGeometry(QRect(220, offset_top + 60, 100, 20))

        self.compl_lbl = QLabel(self.input_box)
        self.compl_lbl.setGeometry(QRect(10, offset_top + 90, 411, 20))
        self.compl_lbl.setText('Объем комплексных услуг')

        self.compl_edit = QLineEdit(self.input_box)
        self.compl_edit.setGeometry(QRect(220, offset_top + 90, 100, 20))

        self.months_lbl = QLabel(self.input_box)
        self.months_lbl.setGeometry(QRect(10, offset_top + 120, 411, 20))
        self.months_lbl.setText('Количество месяцев')

        self.months_edit = QLineEdit(self.input_box)
        self.months_edit.setGeometry(QRect(220, offset_top + 120, 100, 20))

        self.main_dep = QLabel(self.input_box)
        self.main_dep.setGeometry(QRect(10, offset_top + 150, 411, 20))
        self.main_dep.setText('Номер управления')

        self.main_dep_edit = QLineEdit(self.input_box)
        self.main_dep_edit.setGeometry(QRect(220, offset_top + 150, 100, 20))

        self.base_edit = QLineEdit(self.input_box)
        self.base_edit.setGeometry(QRect(220, offset_top + 60, 100, 20))

        self.add_btn = QPushButton('Добавить и расчитать', self.input_box)
        self.add_btn.move(500, 50)

        self.del_btn = QPushButton('Удалить', self.input_box)
        self.del_btn.move(500, 80)

        self.print_btn = QPushButton('Экспортировать в PDF', self.input_box)
        self.print_btn.move(500, 110)

        #self.upd_btn = QPushButton('Обновить', self.input_box)
        #self.upd_btn.move(400, 110)

        # Заполняем бокс с таблицей
        self.coef_table = QTableView(self.db_info_box)
        self.coef_table.setGeometry(QRect(10, 10,
                                            self.db_info_box.width()-20,
                                            self.db_info_box.height()-20)
                                     )

        self.coef_table.setObjectName("coef_table")

        MainWindow.setCentralWidget(self.central_widget)

        QMetaObject.connectSlotsByName(MainWindow)