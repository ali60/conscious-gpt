import sqlite3

class Database:
    def __init__(self):
        self.conn, self.c = self.connect_to_database()

    def connect_to_database(self):
        conn = sqlite3.connect('chat_history.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     question TEXT,
                     answer TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS user_info
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT)''')
        return conn, c

    def get_user_name(self):
        self.c.execute("SELECT name FROM user_info")
        return self.c.fetchone()

    def save_user_name(self, name):
        self.c.execute("INSERT INTO user_info (name) VALUES (?)", (name,))
        self.conn.commit()

    def get_all_questions(self):
        self.c.execute("SELECT question FROM chat_history")
        rows = self.c.fetchall()
        return [row[0] for row in rows]

    def save_question_and_answer(self, question, answer):
        self.c.execute("INSERT INTO chat_history (question, answer) VALUES (?, ?)", (question, answer))
        self.conn.commit()

    def close(self):
        self.conn.close()
