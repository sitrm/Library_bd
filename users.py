import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit
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
        self.setGeometry(100, 100, 800, 600)  #position: x,y len: x,y

        # -----------------------------------------виджеты------------------------------------------
        self.name_label = QLabel('ФИ(Иванов И):', self)
        self.name_label.move(20, 100)
        self.name_entry = QLineEdit(self, placeholderText='name')
        self.name_entry.move(150, 100)


        self.rang_label = QLabel('Ранг:', self)  # TODO: auto rang
        self.rang_label.move(20, 140)
        self.rang_entry = QLineEdit(self, placeholderText='rang')
        self.rang_entry.move(150, 140)

        self.phone_label = QLabel('Номер телефона:', self)  # TODO: auto rang
        self.phone_label.move(20, 180)
        self.phone_entry = QLineEdit(self, placeholderText='phone')
        self.phone_entry.move(150, 180)

        self.delete_button = QPushButton('Удалить читателя', self)

        self.delete_button.setGeometry(380, 108, 150, 30)
        self.delete_button.setStyleSheet('background: rgb(255,0,0);')
        self.delete_button.setStyleSheet("""
        QPushButton{
            font-style: oblique;
            font-weight: bold;
            border: 1px solid #1DA1F2;
            border-radius: 15px;
            color: #1DA1F2;
            background-color: #fff;
        }
        """)
        self.delete_entry = QLineEdit(self, placeholderText='id читателя')
        self.delete_entry.move(550, 100)
        self.delete_button.clicked.connect(self.delete_user)

        # -------------------------------------------кнопки------------------------------------------------
        self.add_button = QPushButton('Добавить читателя', self)
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
        self.show_button.setGeometry(200, 240, 150, 30)
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

        self.sort_button = QPushButton('Отсортировать по рангу', self)
        self.sort_button.setGeometry(20, 280, 170, 30)
        self.sort_button.setStyleSheet("""
        QPushButton{
            font-style: oblique;
            font-weight: bold;
            border: 1px solid #1DA1F2;
            border-radius: 15px;
            color: #1DA1F2;
            background-color: #fff;
        }
        """)
        self.sort_button.clicked.connect(self.sort_user_rang)

        # создаем текстовый виджет для вывода списка людей
        self.output = QTextEdit(self)
        self.output.setGeometry(20, 320, 360, 250)

    # -----------------------------------------------функции-------------------------------------------------
    # функция для добавления книги в базу данных
    def add_reader(self):
        # получаем данные из полей ввода
        name = self.name_entry.text()
        rang = self.rang_entry.text()
        phone = self.phone_entry.text()
        # добавляем книгу в базу данных
        self.cur.execute('INSERT OR REPLACE INTO users (name, rang, phone) VALUES (?, ?, ?)',
                         (name, rang, phone))
        self.conn.commit()
        # очищаем поля ввода!!!!!
        self.name_entry.setText('')
        self.rang_entry.setText('')
        self.phone_entry.setText('')
        self.output.clear()
        self.output.append(f'Пользователь {name} успешно добавлен!')
    # функция для вывода списка читателей из базы данных
    def show_readers(self):
        # получаем всех читателей из базы данных
        self.cur.execute('SELECT * FROM users')
        readers = self.cur.fetchall()
        # очищаем текстовый виджет
        self.output.clear()
        # выводим список книг в текстовый виджет
        for r in readers:
            self.output.append(f'{r[0]}.  {r[1]}, {r[2]}, {r[3]};')

    #удалить пользователя
    def delete_user(self):
        user_id = self.delete_entry.text()
        name_user = self.cur.execute('SELECT name FROM users WHERE user_id = ?', (user_id,)).fetchall()[0][0]
        self.cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        self.conn.commit()
        self.delete_entry.setText('')
        self.cur.execute('SELECT name FROM users WHERE user_id = ?', (user_id,))
        self.output.clear()
        self.output.append(f"Пользователь {name_user} успешно удален!")

    def sort_user_rang(self):
        sort_user = self.cur.execute("SELECT * FROM users ORDER BY rang DESC")
        self.output.clear()
        for cur_sort_user in sort_user:
            self.output.append(f"{cur_sort_user[0]}. {cur_sort_user[1]}, {cur_sort_user[2]}, {cur_sort_user[3]}")


    def closeEvent(self, event):
        # закрываем соединение с базой данных при закрытии приложения
        self.conn.close()

if __name__ == '__main__':
    app = QApplication(
        sys.argv)  # создаем экзэмпляр класса. аргументы sys.argv используются для инициализации QApplication
    book_win = UsersWin()  # создаем обьект класс
    book_win.show()  # выводим его на экран
    sys.exit(app.exec())  # sys.exit() гарантирует, что приложение завершится