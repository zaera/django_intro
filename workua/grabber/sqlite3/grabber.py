import sqlite3


class Sqlite3Grabber:
    def __init__(self, filename=None):
        filename = 'results.db'
        try:
            self.connection = sqlite3.connect(filename)
        except sqlite3.Error as error:
            print("Cannot connect to sqlite", error)  # noqa

    def write(self, item: dict):
        cursor = self.connection.cursor()

        # Create table if not exists

        cursor.execute('''CREATE TABLE IF NOT EXISTS jobs
                        (id integer PRIMARY KEY, id_ integer NOT NULL, title text NOT NULL, description text NOT NULL, city text NOT NULL, salary text NOT NULL)''') # noqa
        self.connection.commit()

        # Check if id is already there

        cursor.execute("""SELECT * FROM jobs WHERE id_=? LIMIT 1""", (item['id'],))
        result = cursor.fetchone()

        if result is None:
            # Write if not

            cursor.execute("""INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?)""",
                           (None, item['id'], item['title'], item['description'], item['city'], item['salary']))
            self.connection.commit()

    def destruct(self):
        self.connection.close()
