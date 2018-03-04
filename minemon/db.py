"""
Handles database stuff
"""

import sqlite3

from minemon import cli


def get_cursor(path):
    """
    Connects to the db and gets a cursor from the connection.
    A cursor was chosen here since it is the recommended approach.
    Likewise, the underlying connection can be used via:
        cursor.connection

    isolation_level=None turns on autocommit. Without it, every
    execution would need to be manually commited and since
    this app doesn't need transactions there is no use in adding
    the extra line of code.
    """
    conn = sqlite3.connect(path, isolation_level=None)
    c = conn.cursor()
    return c


def execute(path, sql, *args, **kwargs):
    """
    Execute some sql.
    Closing the cursor and connection after every execute
    seemed like a good idea since this app is low volume.
    If the number of transactions increased than it should
    be kept open.
    """
    cur = get_cursor(path)
    try:
        res = cur.execute(sql, args or kwargs)
    finally:
        cur.close()
        cur.connection.close()


def create(path):
    """
    Creates the database tables.
    The schema is intended to be used to show the trend over time.
    I imagine we'll be asking questions like:
        How much are we making per month
        How often is the miner down
        What is the average hashrate
    We do not expect sql to do this data crunching for us, but instead
    python. Perhaps in the future this should change.
    """

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
    cur = get_cursor(path)
    cur.execute('SELECT * from stats')
    print('inserted', cur.fetchone())


if __name__ == '__main__':
    args = cli.get_db_args()

    create(args.file)
