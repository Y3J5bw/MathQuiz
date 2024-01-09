# This file is used primarily for database queries requested by the main app
# Hence all database requests go through this class


import sqlite3


class DB:
    """Connection to database is initialised as an instance variable though this is unnecessary as the connection
        does not need to be closed due to there only being one end user ever accessing the sqlite database.
        Speed is not affected so the class is kept for easier management of the code.
    """

    def __init__(self):
        """Establishes the connection to the database and runs a check for if the table exists in the database.
            This check is needed as the connection will create a new database file upon execution if the
            database file does not already exist and this creation cannot be caught in an exception.
        """
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()

        self.cur.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="users"')
        self.check = self.cur.fetchall()

    def initialise(self):
        """Two tables will be used in the database as it will get messy to store the user's score all in one
            table. Using the id method similar to storing orders in an ordering app accessing the data will become
            more efficient. 
        """
        self.cur.execute('CREATE TABLE users (user_id INT NOT NULL, name TEXT, username TEXT, password TEXT)')
        self.cur.execute('CREATE TABLE scores (user_id INT NOT NULL, date TEXT, subject TEXT, score INT)')
        self.con.commit()

    def fetch(self, request_type, user_id=None):
        """Having the data split makes it easier as iterating through a 2d list is comparatively more efficient
            than iterating through a 3d list and filtering out what is not needed.
        :param request_type: string either 'login_creds' or 'scores'
        :param user_id: literally the users id from the database for easy collection of the scores as explained above
        :return: 2d list containing either user login data or scores
        """
        if request_type == 'login_creds':
            self.cur.execute('SELECT * FROM users')
        elif request_type == 'scores':
            self.cur.execute(f'SELECT * FROM scores WHERE user_id={user_id} ORDER BY date ASC')
        data = self.cur.fetchall()
        return data

    def add_user(self, user_id, name, username, password):
        """This function accepts multiple parameters instead of a single list to prevent having to index
            through the list. This approach feels more 'pythonic' as it utilises parameters more to cut down on
            unnecessary code.
        """
        self.cur.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (user_id, name, username, password))
        self.con.commit()

    def add_score(self, user_id, date, subject, score):
        """This function, like the add user function will accept multiple parameters over indexing through
            a list. The code is very similar.
        """
        self.cur.execute('INSERT INTO scores VALUES (?, ?, ?, ?)', (user_id, date, subject, score))
        self.con.commit()
