#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from UI.mainWindowUi import Ui_MainWindow
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5.QtCore import Qt
import datetime
from pdfgen import PrintingWindow
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from shutil import copyfile


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #self.ui.central_widget.setFixedSize()

        self.createConnection()
        #self.fillTable()
        self.createModel()

        self.ui.coef_table.setModel(self.model)

        self.ui.add_btn.clicked.connect(self.addToDb)
        self.ui.del_btn.clicked.connect(self.delrow)
        self.ui.print_btn.clicked.connect(self.openPrintingWindow)

        self.ui.coef_table.setColumnWidth(1, 80)
        self.ui.coef_table.setColumnWidth(2, 40)
        self.ui.coef_table.setColumnWidth(3, 100)
        self.ui.coef_table.setColumnWidth(4, 80)
        self.ui.coef_table.setColumnWidth(5, 100)
        self.ui.coef_table.setColumnWidth(6, 100)
        self.ui.coef_table.setColumnWidth(7, 50)
        self.ui.coef_table.setColumnWidth(8, 120)
        self.ui.coef_table.setColumnWidth(9, 120)
        self.ui.coef_table.hideColumn(0)
        self.printing_window = PrintingWindow()

        self.printing_window.print_btn.clicked.connect(self.printing)

        self.show()
        self.prices_row_count = self.model.rowCount()



    def printing(self):
        pdfmetrics.registerFont(TTFont('Times', 'static/fonts/times.ttf'))
        q = QSqlQuery()

        if self.printing_window.main_dep.text()=='':
            q.exec(
                "SELECT * FROM prices WHERE date BETWEEN '{d1}' AND '{d2}';".format(
                    d1=self.printing_window.start_date_picker.text(),
                    d2=self.printing_window.end_date_picker.text(),
                ))
        else:
            q.exec("SELECT * FROM (SELECT * FROM prices WHERE date BETWEEN '{d1}' AND '{d2}') AS a WHERE a.main_dep = {dep};".format(
                d1=self.printing_window.start_date_picker.text(), d2=self.printing_window.end_date_picker.text(),
                dep=self.printing_window.main_dep.text()
            ))

        top_offset = 60
        doc = SimpleDocTemplate("report.pdf", pagesize=landscape(A4))

        data = [['Услуги', 'Управление', 'Объем компл. \nуслуг',
                 'Базовые норм. \nзатраты', 'Кол-во в \nдер.', 'Кол-во в \nгор.', 'Поправочный \nкоэф.',
                 'Объем фин. \nобеспечения', 'Норм. \nзапраты', 'Кол-во \nмесяцев', 'Дата'],]

        while q.next():
            data.append([str(q.value(1)), str(q.value(2)), str(q.value(3)),
                         str(q.value(4)), str(q.value(5)), str(q.value(6)), str(q.value(7)),
                         str(q.value(8)), str(q.value(9)), str(q.value(10)), str(q.value(11))])

            top_offset += 20

        t = Table(data, style=[('BOX', (0, 0), (-1, -1), 2, colors.black),
                               ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONT', (0, 0), (-1, -1), 'Times',),
                               ('FONTSIZE', (0, 0), (-1, -1), 11),
                               ])

        elements = []
        elements.append(t)
        doc.build(elements)

        pdfCanvas = doc.canv
        pdfCanvas.setTitle('report.pdf')
        self.saveFileDialog()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Экспорт в PDF", "report.pdf",
                                                  "Pdf file (*.pdf)", options=options)
        if fileName:
            print(fileName)
            copyfile('report.pdf', fileName)


    #Открыть окно с генерацией pdf
    def openPrintingWindow(self):
        self.printing_window.show()

    #создаем соединение с БД
    def createConnection(self):

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('socialQt.db')
        self.db.open()

        q = QSqlQuery()
        # Создаем таблицу если ее нет
        q.exec("CREATE TABLE IF NOT EXISTS 'prices'('id' INTEGER, 'name' TEXT, " \
               "'compl_val' INTEGER, " \
               "'main_dep' INTEGER,"
               "'base' INTEGER, " \
               "'village_ammount' INTEGER, " \
               "'city_ammout' INTEGER, " \
               "'coef' INTEGER, " \
               "'total_val' INTEGER, " \
               "'norm_val' INTEGER, " \
               "'months' INTEGER, " \
               "'date' TEXT, " \
               "PRIMARY KEY('id') );")

        while q.next():
            print(q.value(0), q.value(1), q.value(2))


        if not self.db.open():
            print('Cannot establish a database connection')
            return False

    #Создаем модель и ассоциирует ее с tableview
    def createModel(self):
        self.model = QSqlTableModel()
        self.model.setTable('prices')
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(0, Qt.Horizontal, '№')
        self.model.setHeaderData(1, Qt.Horizontal, 'Название')
        self.model.setHeaderData(2, Qt.Horizontal, 'ГУ')
        self.model.setHeaderData(3, Qt.Horizontal, 'Компл. услуги')
        self.model.setHeaderData(4, Qt.Horizontal, 'База, ₽')
        self.model.setHeaderData(5, Qt.Horizontal, 'Кол-во в сёлах')
        self.model.setHeaderData(6, Qt.Horizontal, 'Кол-во в городах')
        self.model.setHeaderData(7, Qt.Horizontal, 'Коэф')
        self.model.setHeaderData(8, Qt.Horizontal, 'Объем средств')
        self.model.setHeaderData(9, Qt.Horizontal, 'Норм. затраты')
        self.model.setHeaderData(10, Qt.Horizontal, 'Кол-во месяцев')
        self.model.setHeaderData(11, Qt.Horizontal, 'Дата')
        #self.model.removeColumn(0)
        self.model.select()

    # Расчет коэффициента
    def coefCount(self, percent, type):
        coef = 0
        if type == 0:
            if percent < 11:
                coef = 1.05
            elif percent < 21:
                coef = 1.13
            elif percent < 31:
                coef = 1.21
            elif percent < 41:
                coef = 1.3
            elif percent < 61:
                coef = 1.42
            elif percent < 81:
                coef = 1.59
            elif percent <= 100:
                coef = 1.76
        else:
            if percent < 11:
                coef = 1.04
            elif percent < 21:
                coef = 1.1
            elif percent < 31:
                coef = 1.16
            elif percent < 41:
                coef = 1.23
            elif percent < 61:
                coef = 1.32
            elif percent < 81:
                coef = 1.45
            elif percent <= 100:
                coef = 1.58

        return coef

    #Запись значений в БД
    def writingRow(self, coef, data, name):
        now = datetime.datetime.now()

        self.model.insertRows(self.prices_row_count, 1)
        self.model.setData(self.model.index(self.prices_row_count, 1),
                           name)
        self.model.setData(self.model.index(self.prices_row_count, 2),
                           data['main_department'])
        self.model.setData(self.model.index(self.prices_row_count, 3),
                           data['compl_val'])
        self.model.setData(self.model.index(self.prices_row_count, 4),
                           data['base_val'])
        self.model.setData(self.model.index(self.prices_row_count, 5),
                           data['village_ammount'])
        self.model.setData(self.model.index(self.prices_row_count, 6),
                           data['city_ammount'])
        self.model.setData(self.model.index(self.prices_row_count, 10),
                           data['months'])
        self.model.setData(self.model.index(self.prices_row_count, 11),
                           now.strftime('%Y-%m-%d'))
        self.model.setData(self.model.index(self.prices_row_count, 7),
                           coef)
        norm_val = data['base_val'] * coef
        norm_val = round(norm_val, 2)
        self.model.setData(self.model.index(self.prices_row_count, 9),
                           norm_val)
        main_value = data['compl_val'] * norm_val / 12 * data['months']
        main_value = round(main_value, 2)
        self.model.setData(self.model.index(self.prices_row_count, 8),
                           round(main_value, 2))
        self.model.submitAll()
        self.prices_row_count += 1




    #Основной метод для записи данных в БД
    def addToDb(self):
        data = {}

        try:
            data['base_val'] = float(self.ui.base_edit.text())
            data['village_ammount'] = float(self.ui.village_number_edit.text())
            data['city_ammount'] = float(self.ui.city_number_edit.text())
            data['months'] = float(self.ui.months_edit.text())
            data['compl_val'] = float(self.ui.compl_edit.text())
            data['main_department'] = float(self.ui.main_dep_edit.text())
            print('збс')
        except:
            QMessageBox.question(
                self,'Внимание!', "Введите числовые данные!",
                QMessageBox.Ok
            )
            return False




        total_ammount = data['village_ammount'] + data['city_ammount']
        village_percent = data['village_ammount'] / total_ammount * 100
        city_percent = data['city_ammount'] / total_ammount * 100
        village_sm_coef = self.coefCount(village_percent, 0)
        village_sb_coef = self.coefCount(village_percent, 1)
        city_sm_coef = self.coefCount(city_percent, 0)
        city_sb_coef = self.coefCount(city_percent, 1)

        self.writingRow(village_sm_coef, data, name='Дер. СМ')
        self.writingRow(village_sb_coef, data, name='Дер. СБ')
        self.writingRow(city_sm_coef, data, name='Гор. СМ')
        self.writingRow(city_sb_coef, data, name='Гор. СБ')





    def delrow(self):
        if self.ui.coef_table.currentIndex().row() > -1:
            self.model.removeRow(self.ui.coef_table.currentIndex().row())
            self.prices_row_count -= 1
            self.model.select()
        else:
            QMessageBox.question(
                self,'Внимание!', "Сначала выберите значение для удаления",
                QMessageBox.Ok
            )
            self.show()

    def updaterow(self):
        if self.ui.coef_table.currentIndex().row() > -1:
            record = self.model.record(self.ui.coef_table.currentIndex().row())
            record.setValue('База, ₽', self.ui.base_edit.text())
            record.setValue('Кол-во в сёлах', self.ui.village_number_edit.text())
            record.setValue('Кол-во в городах', self.ui.city_number_edit.text())
            self.model.setRecord(self.ui.coef_table.currentIndex().row(), record)
        else:
            QMessageBox.question(
                self,'Message', 'Please select a row would you like to update',
                QMessageBox.Ok
            )
            self.show()



    def closeEvent(self, e):
        if (self.db.open()):
            self.db.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())