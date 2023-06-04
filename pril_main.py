import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
from books import BooksWin
from issue import IssueWin
from users import UsersWin
from PyQt6.QtGui import QFont
import sqlite3

#TODO: разбить на файлы классы, посмотреть проверку при выдачи. фоны
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Меню')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()
        
        btn_books = QPushButton('Книги', self)
        btn_books.clicked.connect(self.openBooksWindow)
        btn_users = QPushButton('Пользователи', self)
        btn_users.clicked.connect(self.openUsersWindow)
        btn_issue = QPushButton('Выдача/возврат книг', self)
        btn_issue.clicked.connect(self.openIssueWindow)

        layout.addWidget(btn_books)
        layout.addWidget(btn_users)
        layout.addWidget(btn_issue)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def openBooksWindow(self):
        self.books_window = BooksWin()
        self.books_window.show()

    def openIssueWindow(self):
        self.issue_window = IssueWin()
        self.issue_window.show()

    def openUsersWindow(self):
        self.users_window = UsersWin()
        self.users_window.show()

if __name__ == '__main__':
    app = QApplication(
        sys.argv)  # создаем экзэмпляр класса. аргументы sys.argv используются для инициализации QApplication

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())  # sys.exit() гарантирует, что приложение завершится
    # корректно при завершении цикла обработки событий(app.exec_()).
