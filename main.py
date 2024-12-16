import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidget, QPushButton, QLineEdit, QDialog, QLabel, QTableWidget, QTableWidgetItem

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QSize, Qt

import sqlite3

import csv

class ExampleWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 700, 700)

        ogre = sqlite3.connect('table.sqlite')
        puzo = ogre.cursor()

        aaa = puzo.execute("SELECT * FROM tasks").fetchall()

        rows = len(aaa)
        columns = 5

        self.chupepus = QTableWidget(rows, columns, self)

        self.chupepus.resize(700, 500)


        for i in range(rows):
            self.chupepus.setRowHeight(i, 64)
            zaza = aaa[i]
            for j in range(columns):
                abc = zaza[j]
                stariyboh = str(abc)
                if j == 4:
                    opopopp = QLabel(self.chupepus)
                    kartinka = QPixmap(abc)
                    kartinka = kartinka.scaled(QSize(64, 64))
                    opopopp.setPixmap(kartinka)
                    self.chupepus.setCellWidget(i, j, opopopp)
                else:
                    self.chupepus.setItem(i, j, QTableWidgetItem(stariyboh))

        self.chupepus.move(0, 200)

        self.chupepus.setHorizontalHeaderLabels(['id', 'name', 'category', 'completed', 'image'])

        knopka = QPushButton('добавить задание', self)
        knopka.move(10, 10)

        knopka.clicked.connect(self.ohio)

        self.nazvanie = QLineEdit('', self)
        self.nazvanie.move(10, 40)
        self.kategoria = QLineEdit('', self)
        self.kategoria.move(10, 70)

        knopka.resize(150, 30)

        button = QPushButton('удалить задание', self)
        button.move(10, 100)


        button.clicked.connect(self.skibidi)

        yay = QPushButton('изменить задание', self)
        yay.move(10, 130)

        yay.clicked.connect(self.rizz)


        yay.resize(150, 30)

        text1 = QLabel('название', self)
        text1.move(120, 40)
        text1 = QLabel('категория', self)
        text1.move(120, 70)

        hehe = QPushButton('пометить как сделанное/несделанное', self)
        hehe.move(10, 160)
        hehe.resize(300, 30)

        hehe.clicked.connect(self.kawazaki)

        self.kartinka = QLineEdit('', self)
        self.kartinka.move(220, 40)


        text1 = QLabel('изображение', self)
        text1.move(320, 40)



        save = QPushButton('сохранить в csv', self)
        save.move(400, 100)

        save.clicked.connect(self.pdiddy)

    
    def ohio(self):
        ogre = sqlite3.connect('table.sqlite')
        puzo = ogre.cursor()

        puzo.execute("INSERT INTO tasks (name, category, completed, image) VALUES (?, ?, ?, ?)", (self.nazvanie.text(), self.kategoria.text(), 0, self.kartinka.text()))

        ogre.commit()

        rows = self.chupepus.rowCount() + 1
        columns = 5

        self.chupepus.setRowCount(rows)

        self.chupepus.clear()
        self.chupepus.setHorizontalHeaderLabels(['id', 'name', 'category', 'completed', 'image'])

        aaa = puzo.execute("SELECT * FROM tasks").fetchall()

        for i in range(rows):
            self.chupepus.setRowHeight(i, 64)
            zaza = aaa[i]
            for j in range(columns):
                saslo = zaza[j]
                stariyboh = str(saslo)
                if j == 4:
                    opopopp = QLabel(self.chupepus)
                    kartinka = QPixmap(saslo)
                    kartinka = kartinka.scaled(QSize(64, 64))
                    opopopp.setPixmap(kartinka)
                    self.chupepus.setCellWidget(i, j, opopopp)
                else:
                    self.chupepus.setItem(i, j, QTableWidgetItem(stariyboh))

    def skibidi(self):
        ogre = sqlite3.connect('table.sqlite')
        puzo = ogre.cursor()

        ohh = self.chupepus.selectedIndexes()

        if len(ohh) != 1:
            dialog = QDialog(self)
            QLabel('выберите 1 задание', dialog)


            ashjdjkas = QPushButton('ок', dialog)
            ashjdjkas.clicked.connect(dialog.close)
            ashjdjkas.move(0, 30)

            dialog.show()
        else:
            puzo.execute('DELETE FROM tasks WHERE id = ' + str((self.chupepus.selectedIndexes()[0].row() + 1)))
            ogre.commit()
            
            self.chupepus.removeRow(self.chupepus.selectedIndexes()[0].row())

    def rizz(self):
        ogre = sqlite3.connect('table.sqlite')
        puzo = ogre.cursor()

        ohh = self.chupepus.selectedIndexes()

        if len(ohh) != 1:
            dialog = QDialog(self)
            QLabel('выберите 1 задание', dialog)


            ashjdjkas = QPushButton('ок', dialog)
            ashjdjkas.clicked.connect(dialog.close)
            ashjdjkas.move(0, 30)

            dialog.show()
        else:
            puzo.execute('UPDATE tasks SET name = ?, category = ?, image = ? WHERE id = ?', (self.nazvanie.text(), self.kategoria.text(), self.kartinka.text(), str((self.chupepus.selectedIndexes()[0].row() + 1))))
            ogre.commit()

            self.chupepus.setItem(self.chupepus.selectedIndexes()[0].row(), 1, QTableWidgetItem(str(self.nazvanie.text())))
            self.chupepus.setItem(self.chupepus.selectedIndexes()[0].row(), 2, QTableWidgetItem(str(self.kategoria.text())))
            opopopp = QLabel(self.chupepus)
            kartinka = QPixmap(str(self.kartinka.text()))
            kartinka = kartinka.scaled(QSize(64, 64))
            opopopp.setPixmap(kartinka)
            self.chupepus.setCellWidget(self.chupepus.selectedIndexes()[0].row(), 4, opopopp)

    def kawazaki(self):
        ogre = sqlite3.connect('table.sqlite')
        puzo = ogre.cursor()

        ohh = self.chupepus.selectedIndexes()

        if len(ohh) != 1:
            dialog = QDialog(self)
            QLabel('выберите 1 задание', dialog)


            ashjdjkas = QPushButton('ок', dialog)
            ashjdjkas.clicked.connect(dialog.close)
            ashjdjkas.move(0, 30)

            dialog.show()
        else:
            stolbik = self.chupepus.selectedIndexes()[0].row()

            sdelano = int(self.chupepus.item(stolbik, 3).text())
            id = int(self.chupepus.item(stolbik, 0).text())

            puzo.execute('UPDATE tasks SET completed = ? WHERE id = ?', (1 if sdelano == 0 else 0, id))
            ogre.commit()

            self.chupepus.setItem(stolbik, 3, QTableWidgetItem(str(1 if sdelano == 0 else 0)))

    def pdiddy(self):
        ogre = sqlite3.connect('table.sqlite')
        puzo = ogre.cursor()
        aaa = puzo.execute("SELECT * FROM tasks").fetchall()

        fail = open('vivod.csv', 'w')
        writer = csv.writer(fail)
        writer.writerows(aaa)
        fail.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExampleWindow()
    window.show()
    sys.exit(app.exec())