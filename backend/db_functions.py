import sqlite3
from sqlite3 import connect


def create_databases():
    con = connect("ai_messages.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS ais(id, system_message)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS messages(id, ai_id, time_sent, prompt_role, prompt, response)"
    )


def insert_ai(id: int, system_message: str):
    con = connect("ai_messages.db")
    cur = con.cursor()
    params = (id, system_message)
    cur.execute(f"INSERT INTO ais VALUES(?, ?)", params)
    con.commit()


def select_system_message(ai_id: int):
    con = connect("ai_messages.db")
    cur = con.cursor()
    res = cur.execute("SELECT system_message FROM ais WHERE id=?", (ai_id,))
    return res.fetchone()
