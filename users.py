import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
from PyQt6.QtGui import QFont
import sqlite3

class UsersWin(QMainWindow):

    def __init__(self):
        super().__init__()

        # создаем соединение с нашей базой данных
        self.conn = sqlite3.connect('library.db')
        self.cur = self.conn.cursor()

        self.conn.commit()

        # создаем графический интерфейс
        self.setWindowTitle('Пользователи')
        self.setGeometry(100, 100, 500, 700)  #position: x,y len: x,y

        # -----------------------------------------виджеты------------------------------------------
        self.name_label = QLabel('Имя:', self)
        self.name_label.move(20, 20)
        self.name_entry = QLineEdit(self, placeholderText='name')
        self.name_entry.move(150, 20)

        self.id_label = QLabel('id', self)  # сделать бы автоматическое
        self.id_label.move(20, 60)
        self.id_entry = QLineEdit(self, placeholderText='id')
        self.id_entry.move(150, 60)

        self.book_label = QLabel('Выданная книга:', self)
        self.book_label.move(20, 100)
        self.book_entry = QLineEdit(self, placeholderText='books')
        self.book_entry.move(150, 100)

        self.rang_label = QLabel('Ранг:', self)  # TODO: auto rang
        self.rang_label.move(20, 140)
        self.rang_entry = QLineEdit(self, placeholderText='rang')
        self.rang_entry.move(150, 140)

        self.tel_label = QLabel('Номер телефона:', self)  # TODO: auto rang
        self.tel_label.move(20, 180)
        self.tel_entry = QLineEdit(self, placeholderText='phone')
        self.tel_entry.move(150, 180)

        # -------------------------------------------кнопки------------------------------------------------
        self.add_button = QPushButton('Добавить читателя', self)
        self.add_button.move(20, 240)
        self.add_button.setGeometry(20, 240, 150, 30)
        self.add_button.setStyleSheet('background: rgb(255,0,0);')
        self.add_button.setStyleSheet("""
        QPushButton{
            font-style: oblique;
            font-weight: bold;
            border: 1px solid #1DA1F2;
            border-radius: 15px;
            color: #1DA1F2;
            background-color: #fff;
        }
        """)
        self.add_button.clicked.connect(self.add_reader)

        self.show_button = QPushButton('Показать читателей', self)
        self.show_button.setGeometry(200,240, 150, 30 )
        self.show_button.move(200, 240)
        self.show_button.setStyleSheet("""
        QPushButton{
            font-style: oblique;
            font-weight: bold;
            border: 1px solid #1DA1F2;
            border-radius: 15px;
            color: #1DA1F2;
            background-color: #fff;
        }
        """)
        self.show_button.clicked.connect(self.show_readers)

        # создаем текстовый виджет для вывода списка людей
        self.output = QTextEdit(self)
        self.output.setGeometry(20, 320, 360, 200)

    # -----------------------------------------------функции-------------------------------------------------
    # функция для добавления книги в базу данных
    def add_reader(self):
        # получаем данные из полей ввода
        # получаем данные из полей ввода
        name = self.name_entry.text()
        id = self.id_entry.text()  # TODO: auto id
        rang = self.rang_entry.text()
        book = self.book_entry.text()
        tel = self.tel_entry.text()
        # добавляем книгу в базу данных
        self.cur.execute('INSERT OR REPLACE INTO users (id, name, books, rang, phone number) VALUES (?, ?, ?, ?)',
                         (id, name, book, rang, tel))
        self.conn.commit()
        # очищаем поля ввода!!!!!
        self.name_entry.setText('')
        self.id_entry.setText('')
        self.rang_entry.setText('')
        self.book_entry.setText('')
        self.tel_entry.setText('')
        print('мяу')

    # функция для вывода списка читателей из базы данных
    def show_readers(self):
        # получаем всех читателей из базы данных
        self.cur.execute('SELECT * FROM users')
        readers = self.cur.fetchall()
        # очищаем текстовый виджет
        self.output.clear()
        # выводим список книг в текстовый виджет
        for r in readers:
            self.output.append(f'{r[0]}.  {r[1]}, {r[3]}, {r[4]}, \nчитает: {r[2]}')


    def closeEvent(self, event):
        # закрываем соединение с базой данных при закрытии приложения
        self.conn.close()

if __name__ == '__main__':
    app = QApplication(
        sys.argv)  # создаем экзэмпляр класса. аргументы sys.argv используются для инициализации QApplication
    book_win = UsersWin()  # создаем обьект класс
    book_win.show()  # выводим его на экран
    sys.exit(app.exec())  # sys.exit() гарантирует, что приложение завершится
    # корректно при завершении цикла обработки событий(app.exec_()).