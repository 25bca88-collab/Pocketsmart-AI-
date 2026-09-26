import sqlite3, json
from pathlib import Path
from datetime import datetime
DB_PATH=Path(__file__).resolve().parent/'pocketsmart.db'
def get_connection():
    c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; return c
def create_tables():
    c=get_connection(); x=c.cursor()
    x.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, email TEXT NOT NULL UNIQUE, password TEXT NOT NULL, created_at TEXT NOT NULL)')
    x.execute('CREATE TABLE IF NOT EXISTS recommendations (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, planner_type TEXT NOT NULL, budget TEXT, input_data TEXT, result TEXT, created_at TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))')
    c.commit(); c.close()
def create_user(username,email,password):
    c=get_connection(); c.execute('INSERT INTO users (username,email,password,created_at) VALUES (?,?,?,?)',(username,email,password,datetime.now().isoformat(timespec='seconds'))); c.commit(); c.close()
def get_user(email):
    c=get_connection(); r=c.execute('SELECT * FROM users WHERE email=?',(email,)).fetchone(); c.close(); return dict(r) if r else None
def save_recommendation(user_id,planner_type,budget,input_data,result):
    c=get_connection(); c.execute('INSERT INTO recommendations (user_id,planner_type,budget,input_data,result,created_at) VALUES (?,?,?,?,?,?)',(user_id,planner_type,budget,json.dumps(input_data),result,datetime.now().isoformat(timespec='seconds'))); c.commit(); c.close()
def get_user_history(user_id):
    c=get_connection(); rows=c.execute('SELECT * FROM recommendations WHERE user_id=? ORDER BY id DESC',(user_id,)).fetchall(); c.close(); return [dict(r) for r in rows]
