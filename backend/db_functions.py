from sqlite3 import connect
from time import time


def create_databases():
    with connect("ai_messages.db") as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS ais(id, name, appearance, personality)")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS messages(id integer primary key autoincrement, ai_id, time_sent, role, content)"
        )


def reset_databases():
    with connect("ai_messages.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM ais")
        cur.execute("DELETE FROM messages")


def insert_ai(id: int, name: str, appearance: str, personality: str):
    with connect("ai_messages.db") as con:
        cur = con.cursor()
        params = (id, name, appearance, personality)
        cur.execute("INSERT INTO ais VALUES(?, ?, ?, ?)", params)


def select_system_message_content(ai_id: int):
    with connect("ai_messages.db") as con:
        cur = con.cursor()
        res = cur.execute(
            "SELECT name, appearance, personality FROM ais WHERE id=?", (ai_id,)
        )
        return res.fetchone()


def insert_message(ai_id: int, role: str, content):
    with connect("ai_messages.db") as con:
        cur = con.cursor()
        params = (ai_id, time(), role, content)
        cur.execute(
            "INSERT INTO messages(ai_id, time_sent, role, content) VALUES(?, ?, ?, ?)",
            params,
        )


def select_messages(ai_id: int):
    with connect("ai_messages.db") as con:
        cur = con.cursor()
        res = cur.execute(
            "SELECT role, content FROM messages WHERE ai_id=? ORDER BY time_sent",
            (ai_id,),
        )
        return res.fetchall()
