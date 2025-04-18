import sqlite3
import os
import datetime

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        dirpath = os.path.dirname(self.db_path)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.ensure_tables()

    def ensure_tables(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS time_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                FOREIGN KEY(task_id) REFERENCES tasks(id)
            )
        """)
        self.conn.commit()

    def get_tasks(self):
        c = self.conn.cursor()
        c.execute(
            """
            SELECT t.id, t.name,
                   COALESCE(SUM(strftime('%s', tl.end_time) - strftime('%s', tl.start_time)), 0) as total_seconds
            FROM tasks t
            LEFT JOIN time_logs tl ON t.id = tl.task_id
            GROUP BY t.id
            ORDER BY t.id
            """
        )
        rows = c.fetchall()
        tasks = []
        for row in rows:
            task = {
                'id': row['id'],
                'name': row['name'],
                'total_seconds': int(row['total_seconds'])
            }
            # fetch most recent time log for this task
            c2 = self.conn.cursor()
            c2.execute(
                "SELECT start_time, end_time"
                " FROM time_logs"
                " WHERE task_id = ?"
                " ORDER BY id DESC LIMIT 1",
                (row['id'],)
            )
            lr = c2.fetchone()
            if lr:
                task['last_start'] = lr['start_time']
                task['last_end'] = lr['end_time']
            else:
                task['last_start'] = None
                task['last_end'] = None
            tasks.append(task)
        return tasks

    def add_task(self, name):
        c = self.conn.cursor()
        c.execute("INSERT INTO tasks (name) VALUES (?)", (name,))
        self.conn.commit()
        return c.lastrowid

    def update_task(self, task_id, name):
        c = self.conn.cursor()
        c.execute("UPDATE tasks SET name = ? WHERE id = ?", (name, task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        c.execute("DELETE FROM time_logs WHERE task_id = ?", (task_id,))
        self.conn.commit()

    def start_timer(self, task_id):
        c = self.conn.cursor()
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute("INSERT INTO time_logs (task_id, start_time) VALUES (?, ?)", (task_id, now))
        self.conn.commit()
        return c.lastrowid

    def stop_timer(self, log_id):
        c = self.conn.cursor()
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute("UPDATE time_logs SET end_time = ? WHERE id = ?", (now, log_id))
        self.conn.commit()

    def get_running_timer(self):
        c = self.conn.cursor()
        c.execute(
            "SELECT id, task_id, start_time FROM time_logs WHERE end_time IS NULL ORDER BY id DESC LIMIT 1"
        )
        row = c.fetchone()
        if row:
            return {'id': row['id'], 'task_id': row['task_id'], 'start_time': row['start_time']}
        return None