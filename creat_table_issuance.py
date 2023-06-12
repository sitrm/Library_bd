import sqlite3

# создание базы данных и таблицы
conn = sqlite3.connect('library.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS issue_log
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             user_id INT,
             name_user TEXT,
             name_book TEXT,
             data TEXT,
             FOREIGN KEY(user_id) REFERENCES users(user_id))''')


#cur.execute('DROP TABLE issue_log')
conn.commit()


