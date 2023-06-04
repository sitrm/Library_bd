import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
import sqlite3
from datetime import date

class IssueWin(QMainWindow):
    def __init__(self):
        super().__init__()

        # создаем соединение с нашей базой данных
        self.conn = sqlite3.connect('library.db')
        self.cur = self.conn.cursor()

        self.conn.commit()

        # создаем графический интерфейс
        self.setWindowTitle('Выдача/возврат книг')
        self.setGeometry(50, 50, 500, 500)

        # кнопка выдачи книг
        self.issue_button = QPushButton('Выдать книгу', self)
        self.issue_button.move(20, 100)
        self.issue_button.setStyleSheet("""
        QPushButton{
            font-style: oblique;
            font-weight: bold;
            border: 1px solid #1DA1F2;
            border-radius: 15px;
            color: #1DA1F2;
            background-color: #fff;
        }
        """)
        self.issue_button.clicked.connect(self.issue_book)

        # кнопка возврата книги
        self.return_button = QPushButton('Вернуть книгу', self)
        self.return_button.setStyleSheet("""
                QPushButton{
                    font-style: oblique;
                    font-weight: bold;
                    border: 1px solid #1DA1F2;
                    border-radius: 15px;
                    color: #1DA1F2;
                    background-color: #fff;
                }
                """)
        self.return_button.move(150, 100)
        self.return_button.clicked.connect(self.return_book)

        # создаем текстовый виджет
        self.output = QTextEdit(self)
        self.output.setGeometry(20, 220, 360, 100)


        self.name_book_label = QLabel('Название книги:', self)
        self.name_book_label.move(20, 20)
        #self.name_book_label.setFont(QFont("Times", 8, QFont.italic))
        self.name_book_entry = QLineEdit(self, placeholderText='title')
        self.name_book_entry.move(150, 20)

        self.name_user_label = QLabel('Имя читателя:', self)
        self.name_user_label.move(20, 60)

        self.name_user_entry = QLineEdit(self, placeholderText='users(name)')
        self.name_user_entry.move(150, 60)

    # функция выдачи книг
    def issue_book(self):
        name_book = self.name_book_entry.text()
        name_user = self.name_user_entry.text()
        # проверка на сущетсвование пользователя в БД
        flag = False
        for cur_name_user in self.cur.execute("""SELECT name FROM users""").fetchall():#проходимся циклом по всем пользователям и проверяем
            if cur_name_user[0] == name_user:
                flag = True
        if not flag:
            self.output.clear()
            self.output.append(f"Данного пользователя не существует в базе данных! Добавьте пользователя в базу данных,\
            чтобы выдать книгу!")
            return
        else:
            self.cur.execute('''UPDATE books SET available = 0 
                     WHERE title = ? AND available = 1''', (name_book,))
            # проверка сущетсвования книги в БД
            if self.cur.rowcount == 0:
                self.output.clear()
                self.output.append(f'Этой книги к сожаление нет в библиотеки! Возьмите другую')
                return
            self.cur.execute('''INSERT INTO issue_log (name_user, name_book, data) 
                             VALUES (?, ?, ?)''', (name_user, name_book, date.today()))
            self.conn.commit()
            self.output.clear()
            self.output.append(f'Книга успешно выдана')

    def return_book(self):
        name_book = self.name_book_entry.text()
        self.cur.execute('''SELECT * FROM issue_log WHERE name_book = ?''', (name_book,))
        issue = self.cur.fetchone()
        if issue is None:
            self.output.clear()
            self.output.append(f'Книга уже возвращена!')
            return
        self.cur.execute('''UPDATE books SET available = 1 WHERE title = ?''', (name_book,))
        self.cur.execute('''DELETE FROM issue_log WHERE id = ?''', (issue[0],))
        self.conn.commit()
        self.output.clear()
        self.output.append(f'Книга {name_book} успешно возвращена!')

    def closeEvent(self, event):
        # закрываем соединение с базой данных при закрытии приложения
        self.conn.close()

if __name__ == '__main__':
    app = QApplication(
        sys.argv)  # создаем экзэмпляр класса. аргументы sys.argv используются для инициализации QApplication
    issue_win = IssueWin()  # создаем обьект класс
    issue_win.show()  # выводим его на экран
    sys.exit(app.exec())  # sys.exit() гарантирует, что приложение завершится
    # корректно при завершении цикла обработки событий(app.exec_()).