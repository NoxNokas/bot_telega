import sqlite3
import functools


def init_db(force: bool = False):
    """
    Checking that the required tables exist, otherwise delete them
    Args:
        force: will explicitly recreate all tables

    Returns: None

    """

    conn = sqlite3.connect('users_and_actions.db')
    c = conn.cursor()

    if force:
        c.execute('''DROP TABLE IF EXISTS users''')
        c.execute('''DROP TABLE IF EXISTS actions''')

    # Create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id          INT PRIMARY KEY,
            name        TEXT NOT NULL
        )
    ''')

    c.execute(
        '''CREATE TABLE IF NOT EXISTS actions (
            user_id INT NOT NULL, 
            action TEXT NOT NULL, 
            FOREIGN KEY (user_id) REFERENCES users(id))
        ''')

    # Save (commit) the changes
    conn.commit()


def insert_db(func):
    @functools.wraps(func)
    def wrapped(updater, context):
        func(updater, context)

        conn = sqlite3.connect('users_and_actions.db')
        c = conn.cursor()

        user_id = updater['message']['chat']['id']
        user_name = updater['message']['chat']['first_name']
        action = updater['message']['text']

        c.execute("""SELECT id FROM users WHERE id = {0}""".format(user_id))
        if len(c.fetchall()) == 0:
            c.execute("""INSERT INTO users VALUES ({0}, '{1}')""".format(user_id, user_name))
        c.execute("""INSERT INTO actions VALUES ({0}, '{1}')""".format(user_id, action))
        conn.commit()

    return wrapped
