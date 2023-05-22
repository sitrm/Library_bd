import sqlite3

# создание базы данных и таблицы
conn = sqlite3.connect('library.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS issues 
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              b_id INTEGER,
              u_id INTEGER,
              FOREIGN KEY(b_id) REFERENCES books(book_id),
              FOREIGN KEY(u_id) REFERENCES readers(user_id))''')
conn.commit()