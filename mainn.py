import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidget, QPushButton, QLineEdit, QDialog, QLabel, \
    QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QSize, Qt
import sqlite3
import csv

class ExampleWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Устанавливаем размеры и положение окна
        self.setGeometry(300, 300, 700, 700)

        # Подключаемся к базе данных SQLite
        ogre = sqlite3.connect('table.sqlite')
        puzo = ogre.cursor()

        # Получаем данные из таблиц tasks и categories
        aaa = puzo.execute("SELECT * FROM tasks").fetchall()
        bbb = puzo.execute("SELECT * FROM categories").fetchall()

        # Создаем таблицу для отображения задач
        rows = len(aaa)
        columns = 5
        self.chupepus = QTableWidget(rows, columns, self)
        self.chupepus.resize(500, 500)

        # Заполняем таблицу данными из базы данных
        for i in range(rows):
            self.chupepus.setRowHeight(i, 64)
            zaza = aaa[i]
            for j in range(columns):
                abc = zaza[j]
                stariyboh = str(abc)
                if j == 4:  # Если это столбец с изображением, создаем QLabel с изображением
                    opopopp = QLabel(self.chupepus)
                    kartinka = QPixmap(abc)
                    kartinka = kartinka.scaled(QSize(64, 64))
                    opopopp.setPixmap(kartinka)
                    self.chupepus.setCellWidget(i, j, opopopp)
                else:  # Иначе просто добавляем текстовое значение
                    self.chupepus.setItem(i, j, QTableWidgetItem(stariyboh))

        self.chupepus.move(0, 200)
        self.chupepus.setHorizontalHeaderLabels(['id', 'name', 'category', 'completed', 'image'])

        # Создаем таблицу для отображения категорий
        self.cattable = QTableWidget(len(bbb), 2, self)
        self.cattable.move(500, 200)
        self.cattable.resize(200, 500)
        self.cattable.setHorizontalHeaderLabels(['id', 'name'])

        # Заполняем таблицу категорий данными из базы данных
        for i in range(len(bbb)):
            for j in range(2):
                self.cattable.setItem(i, j, QTableWidgetItem(str(bbb[i][j])))

        # Создаем кнопку для добавления задачи
        knopka = QPushButton('добавить задание', self)
        knopka.move(10, 10)
        knopka.clicked.connect(self.ohio)

        # Создаем поля ввода для названия задачи и категории
        self.nazvanie = QLineEdit('', self)
        self.nazvanie.move(10, 40)
        self.kategoria = QLineEdit('', self)
        self.kategoria.move(10, 70)

        knopka.resize(150, 30)

        # Создаем кнопку для удаления задачи
        button = QPushButton('удалить задание', self)
        button.move(10, 100)
        button.clicked.connect(self.skibidi)

        # Создаем кнопку для изменения задачи
        yay = QPushButton('изменить задание', self)
        yay.move(10, 130)
        yay.clicked.connect(self.rizz)
        yay.resize(150, 30)

        # Создаем метки для полей ввода
        text1 = QLabel('название', self)
        text1.move(120, 40)
        text1 = QLabel('id категории', self)
        text1.move(120, 70)

        # Создаем кнопку для отметки задачи как выполненной/невыполненной
        hehe = QPushButton('пометить как сделанное/несделанное', self)
        hehe.move(10, 160)
        hehe.resize(300, 30)
        hehe.clicked.connect(self.kawazaki)

        # Создаем поле ввода для пути к изображению
        self.kartinka = QLineEdit('', self)
        self.kartinka.move(220, 40)
        text1 = QLabel('изображение', self)
        text1.move(320, 40)

        # Создаем кнопку для сохранения данных в CSV-файл
        save = QPushButton('сохранить в csv', self)
        save.move(400, 160)
        save.clicked.connect(self.pdiddy)

        # Создаем поле ввода и кнопку для добавления новой категории
        text1 = QLabel('название категории', self)
        text1.move(520, 30)
        text1.resize(150, 50)
        self.catnameinp = QLineEdit('', self)
        self.catnameinp.move(420, 40)
        iii = QPushButton('добавить категорию', self)
        iii.move(420, 80)
        iii.resize(150, 20)
        iii.clicked.connect(self.addcatbtn)

    def addcatbtn(self):
        # Добавляем новую категорию в базу данных
        ogre = sqlite3.connect('table.sqlite')
        puzo = ogre.cursor()

        puzo.execute('INSERT INTO categories (name) VALUES (?)', (self.catnameinp.text(),))
        ogre.commit()

        # Обновляем таблицу категорий
        nrc = self.cattable.rowCount() + 1
        self.cattable.setRowCount(nrc)
        self.cattable.setItem(nrc - 1, 0, QTableWidgetItem(str(nrc - 1)))
        self.cattable.setItem(nrc - 1, 1, QTableWidgetItem(str(self.catnameinp.text())))

    def ohio(self):
        # Добавляем новую задачу в базу данных
        ogre = sqlite3.connect('table.sqlite')
        puzo = ogre.cursor()

        try:
            catint = int(self.kategoria.text())
        except Exception as e:
            # Если категория не является числом, показываем диалоговое окно с ошибкой
            dialog = QDialog(self)
            QLabel('категория не число', dialog)
            ashjdjkas = QPushButton('ок', dialog)
            ashjdjkas.clicked.connect(dialog.close)
            ashjdjkas.move(0, 30)
            dialog.show()
            return

        # Проверяем, существует ли категория с таким id
        bbb = puzo.execute("SELECT * FROM categories").fetchall()
        ok = False
        for zzz in bbb:
            if zzz[0] == catint:
                ok = True
                break
        if not ok:
            # Если категория не существует, показываем диалоговое окно с ошибкой
            dialog = QDialog(self)
            QLabel('такой категории нет', dialog)
            ashjdjkas = QPushButton('ок', dialog)
            ashjdjkas.clicked.connect(dialog.close)
            ashjdjkas.move(0, 30)
            dialog.show()
            return

        # Добавляем задачу в базу данных
        puzo.execute("INSERT INTO tasks (name, category, completed, image) VALUES (?, ?, ?, ?)",
                     (self.nazvanie.text(), self.kategoria.text(), 0, self.kartinka.text()))
        ogre.commit()

        # Обновляем таблицу задач
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
        # Удаляем выбранную задачу из базы данных
        ogre = sqlite3.connect('table.sqlite')
        puzo = ogre.cursor()

        ohh = self.chupepus.selectedIndexes()

        if len(ohh) != 1:
            # Если выбрано не одно задание, показываем диалоговое окно с ошибкой
            dialog = QDialog(self)
            QLabel('выберите 1 задание', dialog)
            ashjdjkas = QPushButton('ок', dialog)
            ashjdjkas.clicked.connect(dialog.close)
            ashjdjkas.move(0, 30)
            dialog.show()
        else:
            # Удаляем задачу из базы данных и обновляем таблицу
            puzo.execute('DELETE FROM tasks WHERE id = ' + str((self.chupepus.selectedIndexes()[0].row() + 1)))
            ogre.commit()
            self.chupepus.removeRow(self.chupepus.selectedIndexes()[0].row())

    def rizz(self):
        # Изменяем выбранную задачу в базе данных
        ogre = sqlite3.connect('table.sqlite')
        puzo = ogre.cursor()

        ohh = self.chupepus.selectedIndexes()

        if len(ohh) != 1:
            # Если выбрано не одно задание, показываем диалоговое окно с ошибкой
            dialog = QDialog(self)
            QLabel('выберите 1 задание', dialog)
            ashjdjkas = QPushButton('ок', dialog)
            ashjdjkas.clicked.connect(dialog.close)
            ashjdjkas.move(0, 30)
            dialog.show()
        else:
            try:
                catint = int(self.kategoria.text())
            except Exception as e:
                # Если категория не является числом, показываем диалоговое окно с ошибкой
                dialog = QDialog(self)
                QLabel('категория не число', dialog)
                ashjdjkas = QPushButton('ок', dialog)
                ashjdjkas.clicked.connect(dialog.close)
                ashjdjkas.move(0, 30)
                dialog.show()
                return

            # Проверяем, существует ли категория с таким id
            bbb = puzo.execute("SELECT * FROM categories").fetchall()
            ok = False
            for zzz in bbb:
                if zzz[0] == catint:
                    ok = True
                    break
            if not ok:
                # Если категория не существует, показываем диалоговое окно с ошибкой
                dialog = QDialog(self)
                QLabel('такой категории нет', dialog)
                ashjdjkas = QPushButton('ок', dialog)
                ashjdjkas.clicked.connect(dialog.close)
                ashjdjkas.move(0, 30)
                dialog.show()
                return

            # Обновляем задачу в базе данных
            puzo.execute('UPDATE tasks SET name = ?, category = ?, image = ? WHERE id = ?', (
                self.nazvanie.text(), self.kategoria.text(), self.kartinka.text(),
                str((self.chupepus.selectedIndexes()[0].row() + 1))))
            ogre.commit()

            # Обновляем таблицу задач
            self.chupepus.setItem(self.chupepus.selectedIndexes()[0].row(), 1,
                                  QTableWidgetItem(str(self.nazvanie.text())))
            self.chupepus.setItem(self.chupepus.selectedIndexes()[0].row(), 2,
                                  QTableWidgetItem(str(self.kategoria.text())))
            opopopp = QLabel(self.chupepus)
            kartinka = QPixmap(str(self.kartinka.text()))
            kartinka = kartinka.scaled(QSize(64, 64))
            opopopp.setPixmap(kartinka)
            self.chupepus.setCellWidget(self.chupepus.selectedIndexes()[0].row(), 4, opopopp)

    def kawazaki(self):
        # Изменяем статус задачи (выполнено/не выполнено)
        ogre = sqlite3.connect('table.sqlite')
        puzo = ogre.cursor()

        ohh = self.chupepus.selectedIndexes()

        if len(ohh) != 1:
            # Если выбрано не одно задание, показываем диалоговое окно с ошибкой
            dialog = QDialog(self)
            QLabel('выберите 1 задание', dialog)
            ashjdjkas = QPushButton('ок', dialog)
            ashjdjkas.clicked.connect(dialog.close)
            ashjdjkas.move(0, 30)
            dialog.show()
        else:
            # Изменяем статус задачи в базе данных и обновляем таблицу
            stolbik = self.chupepus.selectedIndexes()[0].row()
            sdelano = int(self.chupepus.item(stolbik, 3).text())
            id = int(self.chupepus.item(stolbik, 0).text())

            puzo.execute('UPDATE tasks SET completed = ? WHERE id = ?', (1 if sdelano == 0 else 0, id))
            ogre.commit()

            self.chupepus.setItem(stolbik, 3, QTableWidgetItem(str(1 if sdelano == 0 else 0)))

    def pdiddy(self):
        # Сохраняем данные из таблицы задач в CSV-файл
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