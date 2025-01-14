import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QDialog, QLabel, \
    QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QSize
import sqlite3
import csv


class ExampleWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Устанавливаем размеры и положение окна
        self.setGeometry(300, 300, 700, 700)

        # Подключаемся к базе данных SQLite
        db_connection = sqlite3.connect('table.sqlite')
        db_cursor = db_connection.cursor()

        # Получаем данные из таблиц tasks и categories
        tasks_data = db_cursor.execute("SELECT * FROM tasks").fetchall()
        categories_data = db_cursor.execute("SELECT * FROM categories").fetchall()

        # Создаем таблицу для отображения задач
        tasks_rows = len(tasks_data)
        tasks_columns = 5
        self.tasks_table = QTableWidget(tasks_rows, tasks_columns, self)
        self.tasks_table.resize(500, 500)

        # Заполняем таблицу данными из базы данных
        for row in range(tasks_rows):
            self.tasks_table.setRowHeight(row, 64)
            task = tasks_data[row]
            for column in range(tasks_columns):
                cell_data = task[column]
                cell_data_str = str(cell_data)
                if column == 4:  # Если это столбец с изображением, создаем QLabel с изображением
                    image_label = QLabel(self.tasks_table)
                    image = QPixmap(cell_data)
                    image = image.scaled(QSize(64, 64))
                    image_label.setPixmap(image)
                    self.tasks_table.setCellWidget(row, column, image_label)
                else:  # Иначе просто добавляем текстовое значение
                    self.tasks_table.setItem(row, column, QTableWidgetItem(cell_data_str))

        self.tasks_table.move(0, 200)
        self.tasks_table.setHorizontalHeaderLabels(['id', 'name', 'category', 'completed', 'image'])

        # Создаем таблицу для отображения категорий
        self.categories_table = QTableWidget(len(categories_data), 2, self)
        self.categories_table.move(500, 200)
        self.categories_table.resize(200, 500)
        self.categories_table.setHorizontalHeaderLabels(['id', 'name'])

        # Заполняем таблицу категорий данными из базы данных
        for row in range(len(categories_data)):
            for column in range(2):
                self.categories_table.setItem(row, column, QTableWidgetItem(str(categories_data[row][column])))

        # Создаем кнопку для добавления задачи
        add_task_button = QPushButton('добавить задание', self)
        add_task_button.move(10, 10)
        add_task_button.clicked.connect(self.add_task)

        # Создаем поля ввода для названия задачи и категории
        self.task_name_input = QLineEdit('', self)
        self.task_name_input.move(10, 40)
        self.task_category_input = QLineEdit('', self)
        self.task_category_input.move(10, 70)

        add_task_button.resize(150, 30)

        # Создаем кнопку для удаления задачи
        delete_task_button = QPushButton('удалить задание', self)
        delete_task_button.move(10, 100)
        delete_task_button.clicked.connect(self.delete_task)

        # Создаем кнопку для изменения задачи
        edit_task_button = QPushButton('изменить задание', self)
        edit_task_button.move(10, 130)
        edit_task_button.clicked.connect(self.edit_task)
        edit_task_button.resize(150, 30)

        # Создаем метки для полей ввода
        task_name_label = QLabel('название', self)
        task_name_label.move(120, 40)
        task_category_label = QLabel('id категории', self)
        task_category_label.move(120, 70)

        # Создаем кнопку для отметки задачи как выполненной/невыполненной
        toggle_task_status_button = QPushButton('пометить как сделанное/несделанное', self)
        toggle_task_status_button.move(10, 160)
        toggle_task_status_button.resize(300, 30)
        toggle_task_status_button.clicked.connect(self.toggle_task_status)

        # Создаем поле ввода для пути к изображению
        self.task_image_input = QLineEdit('', self)
        self.task_image_input.move(220, 40)
        task_image_label = QLabel('изображение', self)
        task_image_label.move(320, 40)

        # Создаем кнопку для сохранения данных в CSV-файл
        save_to_csv_button = QPushButton('сохранить в csv', self)
        save_to_csv_button.move(400, 160)
        save_to_csv_button.clicked.connect(self.save_to_csv)

        # Создаем поле ввода и кнопку для добавления новой категории
        category_name_label = QLabel('название категории', self)
        category_name_label.move(520, 30)
        category_name_label.resize(150, 50)
        self.category_name_input = QLineEdit('', self)
        self.category_name_input.move(420, 40)
        add_category_button = QPushButton('добавить категорию', self)
        add_category_button.move(420, 80)
        add_category_button.resize(150, 20)
        add_category_button.clicked.connect(self.add_category)

    def add_category(self):
        # Добавляем новую категорию в базу данных
        db_connection = sqlite3.connect('table.sqlite')
        db_cursor = db_connection.cursor()

        db_cursor.execute('INSERT INTO categories (name) VALUES (?)', (self.category_name_input.text(),))
        db_connection.commit()

        # Обновляем таблицу категорий
        new_row_count = self.categories_table.rowCount() + 1
        self.categories_table.setRowCount(new_row_count)
        self.categories_table.setItem(new_row_count - 1, 0, QTableWidgetItem(str(new_row_count - 1)))
        self.categories_table.setItem(new_row_count - 1, 1, QTableWidgetItem(str(self.category_name_input.text())))

    def add_task(self):
        # Добавляем новую задачу в базу данных
        db_connection = sqlite3.connect('table.sqlite')
        db_cursor = db_connection.cursor()

        try:
            category_id = int(self.task_category_input.text())
        except Exception as e:
            # Если категория не является числом, показываем диалоговое окно с ошибкой
            error_dialog = QDialog(self)
            QLabel('категория не число', error_dialog)
            ok_button = QPushButton('ок', error_dialog)
            ok_button.clicked.connect(error_dialog.close)
            ok_button.move(0, 30)
            error_dialog.show()
            return

        # Проверяем, существует ли категория с таким id
        categories_data = db_cursor.execute("SELECT * FROM categories").fetchall()
        category_exists = False
        for category in categories_data:
            if category[0] == category_id:
                category_exists = True
                break
        if not category_exists:
            # Если категория не существует, показываем диалоговое окно с ошибкой
            error_dialog = QDialog(self)
            QLabel('такой категории нет', error_dialog)
            ok_button = QPushButton('ок', error_dialog)
            ok_button.clicked.connect(error_dialog.close)
            ok_button.move(0, 30)
            error_dialog.show()
            return

        # Добавляем задачу в базу данных
        db_cursor.execute("INSERT INTO tasks (name, category, completed, image) VALUES (?, ?, ?, ?)",
                          (self.task_name_input.text(), self.task_category_input.text(), 0, self.task_image_input.text()))
        db_connection.commit()

        # Обновляем таблицу задач
        new_row_count = self.tasks_table.rowCount() + 1
        self.tasks_table.setRowCount(new_row_count)
        self.tasks_table.clear()  # Очищаем таблицу перед обновлением
        self.tasks_table.setHorizontalHeaderLabels(['id', 'name', 'category', 'completed', 'image'])

        tasks_data = db_cursor.execute("SELECT * FROM tasks").fetchall()
        for row in range(new_row_count):
            self.tasks_table.setRowHeight(row, 64)  # Устанавливаем высоту строки
            task = tasks_data[row]
            for column in range(5):
                cell_data = task[column]
                cell_data_str = str(cell_data)
                if column == 4:
                    image_label = QLabel(self.tasks_table)
                    image = QPixmap(cell_data)
                    image = image.scaled(QSize(64, 64))
                    image_label.setPixmap(image)
                    self.tasks_table.setCellWidget(row, column, image_label)
                else:
                    self.tasks_table.setItem(row, column, QTableWidgetItem(cell_data_str))

    def delete_task(self):
        # Удаляем выбранную задачу из базы данных
        db_connection = sqlite3.connect('table.sqlite')
        db_cursor = db_connection.cursor()

        selected_indexes = self.tasks_table.selectedIndexes()

        if len(selected_indexes) != 1:
            # Если выбрано не одно задание, показываем диалоговое окно с ошибкой
            error_dialog = QDialog(self)
            QLabel('выберите 1 задание', error_dialog)
            ok_button = QPushButton('ок', error_dialog)
            ok_button.clicked.connect(error_dialog.close)
            ok_button.move(0, 30)
            error_dialog.show()
        else:
            # Удаляем задачу из базы данных и обновляем таблицу
            db_cursor.execute('DELETE FROM tasks WHERE id = ' + str((self.tasks_table.selectedIndexes()[0].row() + 1)))
            db_connection.commit()
            self.tasks_table.removeRow(self.tasks_table.selectedIndexes()[0].row())

    def edit_task(self):
        # Изменяем выбранную задачу в базе данных
        db_connection = sqlite3.connect('table.sqlite')
        db_cursor = db_connection.cursor()

        selected_indexes = self.tasks_table.selectedIndexes()

        if len(selected_indexes) != 1:
            # Если выбрано не одно задание, показываем диалоговое окно с ошибкой
            error_dialog = QDialog(self)
            QLabel('выберите 1 задание', error_dialog)
            ok_button = QPushButton('ок', error_dialog)
            ok_button.clicked.connect(error_dialog.close)
            ok_button.move(0, 30)
            error_dialog.show()
        else:
            try:
                category_id = int(self.task_category_input.text())
            except Exception as e:
                # Если категория не является числом, показываем диалоговое окно с ошибкой
                error_dialog = QDialog(self)
                QLabel('категория не число', error_dialog)
                ok_button = QPushButton('ок', error_dialog)
                ok_button.clicked.connect(error_dialog.close)
                ok_button.move(0, 30)
                error_dialog.show()
                return

            # Проверяем, существует ли категория с таким id
            categories_data = db_cursor.execute("SELECT * FROM categories").fetchall()
            category_exists = False
            for category in categories_data:
                if category[0] == category_id:
                    category_exists = True
                    break
            if not category_exists:
                # Если категория не существует, показываем диалоговое окно с ошибкой
                error_dialog = QDialog(self)
                QLabel('такой категории нет', error_dialog)
                ok_button = QPushButton('ок', error_dialog)
                ok_button.clicked.connect(error_dialog.close)
                ok_button.move(0, 30)
                error_dialog.show()
                return

            # Обновляем задачу в базе данных
            db_cursor.execute('UPDATE tasks SET name = ?, category = ?, image = ? WHERE id = ?', (
                self.task_name_input.text(), self.task_category_input.text(), self.task_image_input.text(),
                str((self.tasks_table.selectedIndexes()[0].row() + 1))))
            db_connection.commit()

            # Обновляем таблицу задач
            self.tasks_table.setItem(self.tasks_table.selectedIndexes()[0].row(), 1,
                                    QTableWidgetItem(str(self.task_name_input.text())))
            self.tasks_table.setItem(self.tasks_table.selectedIndexes()[0].row(), 2,
                                    QTableWidgetItem(str(self.task_category_input.text())))
            image_label = QLabel(self.tasks_table)
            image = QPixmap(str(self.task_image_input.text()))
            image = image.scaled(QSize(64, 64))
            image_label.setPixmap(image)
            self.tasks_table.setCellWidget(self.tasks_table.selectedIndexes()[0].row(), 4, image_label)

    def toggle_task_status(self):
        # Изменяем статус задачи (выполнено/не выполнено)
        db_connection = sqlite3.connect('table.sqlite')
        db_cursor = db_connection.cursor()

        selected_indexes = self.tasks_table.selectedIndexes()

        if len(selected_indexes) != 1:
            # Если выбрано не одно задание, показываем диалоговое окно с ошибкой
            error_dialog = QDialog(self)
            QLabel('выберите 1 задание', error_dialog)
            ok_button = QPushButton('ок', error_dialog)
            ok_button.clicked.connect(error_dialog.close)
            ok_button.move(0, 30)
            error_dialog.show()
        else:
            # Изменяем статус задачи в базе данных и обновляем таблицу
            selected_row = self.tasks_table.selectedIndexes()[0].row()
            current_status = int(self.tasks_table.item(selected_row, 3).text())
            task_id = int(self.tasks_table.item(selected_row, 0).text())

            db_cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (1 if current_status == 0 else 0, task_id))
            db_connection.commit()

            self.tasks_table.setItem(selected_row, 3, QTableWidgetItem(str(1 if current_status == 0 else 0)))

    def save_to_csv(self):
        # Сохраняем данные из таблицы задач в CSV-файл
        db_connection = sqlite3.connect('table.sqlite')
        db_cursor = db_connection.cursor()
        tasks_data = db_cursor.execute("SELECT * FROM tasks").fetchall()

        with open('tasks_export.csv', 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(tasks_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExampleWindow()
    window.show()
    sys.exit(app.exec())