"""
Handles database stuff
"""

import sqlite3

from minemon import cli


def get_connection(path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    return c


def execute(path, sql, *args, **kwargs):
    conn = get_connection(path)
    try:
        print(sql, args)
        res = conn.execute(sql, args or kwargs)
        print(res)
    finally:
        conn.close()
        conn.connection.close()


def create(path):
    execute(path, '''
            CREATE TABLE IF NOT EXISTS stats(
                date TEXT,
                hashrate INTEGER,
                is_down INTEGER,
                balance TEXT,
                total_paid TEXT
            );
        ''')


def insert(path, *, date, hashrate, is_down, balance, total_paid):
    execute(path, '''
        INSERT into stats(
            date,
            hashrate,
            is_down,
            balance,
            total_paid
        )
        values (?, ?, ?, ?, ?)
        ''', date, hashrate, is_down, balance, total_paid)
    conn = get_connection(path)
    print(conn.fetchone())


if __name__ == '__main__':
    args = cli.get_db_args()

    create(args.file)
