# sqlite-demo.py

from sqlite3 import connect

# from contextlib import contextmanager

from time import time

from time import sleep

from random import random


def create_db():
    with connect("test.db") as conn:
        cur = conn.cursor()
        cur.execute("create table IF NOT EXISTS points(x int, y int)")


def destroy_db():
    with connect("test.db") as conn:
        cur = conn.cursor()
        cur.execute("drop table points")


def write_to_db(value):
    with connect("test.db") as conn:
        cur = conn.cursor()
        sql = "insert into points (x, y) values(?,?)"
        point = (time(), value)
        cur.execute(sql, point)


def sample_device(sample_count):
    for i in range(sample_count):
        value = random() * 10 + 15
        write_to_db(value)
        print(str(i) + " wrote: " + str(value))
        sleep(1)


if __name__ == "__main__":
    # create_db()
    sample_device(5)
