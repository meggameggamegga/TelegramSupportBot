import sqlite3


class DataBase:
    def __init__(self, db_file):
        self.connect = sqlite3.connect(db_file)
        self.cursor = self.connect.cursor()
        self.create_table()

    def create_table(self):
        '''
        :param:role - admin ,user,banned
        :param:status_ticket - 0 ожидает ответ от админа, 1 ответ от клиента
        '''
        with self.connect:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            user_id INTEGER,
                                            username TEXT,
                                            role TEXT DEFAULT "user",
                                            ticket INTEGER NULL,
                                            status_ticket INTEGER NULL,
                                            msg_ticket INTEGER NULL
                                        )''')

    def user_exist(self, user_id):
        with self.connect:
            data = self.cursor.execute('''SELECT user_id FROM user WHERE user_id=(?)''',
                                       [user_id]).fetchall()
            return data if data else False

    def add_user(self, user_id, username):
        with self.connect:
            return self.cursor.execute('''INSERT INTO user(user_id,username) VALUES (?,?)''',
                                       [user_id, username])

    def add_ticket_to_user(self, user_id, ticket: int):
        with self.connect:
            return self.cursor.execute('''UPDATE user SET ticket=(?) WHERE user_id=(?)''',
                                       [ticket, user_id])

    def get_user_ticket(self, user_id):
        with self.connect:
            return self.cursor.execute('''SELECT ticket FROM user WHERE user_id=(?)''',
                                       [user_id]).fetchone()[0]

    def set_status_ticket(self, status, user_id=None, ticket=None):
        with self.connect:
            if user_id:
                return self.cursor.execute('''UPDATE user SET status_ticket=(?) WHERE user_id=(?)''',
                                           [status, user_id])
            else:
                return self.cursor.execute('''UPDATE user SET status_ticket=(?) WHERE ticket=(?)''',
                                           [status, ticket])

    def set_msg_ticket(self, msg_ticket, user_id=None, ticket=None):
        with self.connect:
            if user_id:
                return self.cursor.execute('''UPDATE user SET msg_ticket=? WHERE user_id=?''',
                                           [msg_ticket, user_id])
            else:
                return self.cursor.execute('''UPDATE user SET msg_ticket=? WHERE ticket=?''',
                                           [msg_ticket, ticket])

    def get_ticket_status(self, ticket=None, user_id=None):
        with self.connect:
            if ticket:
                return self.cursor.execute('''SELECT status_ticket FROM user WHERE ticket=(?)''',
                                           [ticket]).fetchone()[0]
            else:
                return self.cursor.execute('''SELECT status_ticket FROM user WHERE user_id=(?)''',
                                           [user_id]).fetchone()[0]

    def get_ticket_owner(self, ticket):
        with self.connect:
            return self.cursor.execute('''SELECT user_id FROM user WHERE ticket=(?)''',
                                       [ticket]).fetchone()[0]

    def get_msg_status(self, ticket=None, user_id=None):
        with self.connect:
            if ticket:
                return self.cursor.execute('''SELECT msg_ticket FROM user WHERE ticket=(?)''',
                                           [ticket]).fetchone()[0]
            else:
                return self.cursor.execute('''SELECT msg_ticket FROM user WHERE user_id=(?)''',
                                           [user_id]).fetchone()[0]

    def delete_ticket(self, user_id=None, ticket=None):
        with self.connect:
            if ticket:
                return self.connect.execute(
                    '''UPDATE user SET ticket = NULL,status_ticket = NULL,msg_ticket = NULL WHERE ticket=(?)''',
                    [ticket])
            else:
                return self.connect.execute(
                    '''UPDATE user SET ticket = NULL,status_ticket = NULL,msg_ticket = NULL WHERE user_id=(?)''',
                    [user_id])

    def get_all_tickets(self):
        with self.connect:
            return self.cursor.execute('''SELECT * FROM user WHERE ticket IS NOT NULL''').fetchall()

    def get_ticket_id_ticket(self, ticket):
        with self.connect:
            return self.cursor.execute('''SELECT id FROM user WHERE ticket = (?)''',
                                       [ticket]).fetchone()[0]

    def set_user_role(self, user_id, role):
        with self.connect:
            return self.cursor.execute('''UPDATE user SET role = (?) WHERE id=(?)''',
                                       [role, user_id])

    def get_role_user(self, user_id):
        with self.connect:
            return self.cursor.execute('''SELECT role FROM user WHERE user_id = (?)''',
                                       [user_id]).fetchone()[0]

    def get_all_users(self):
        with self.connect:
            return self.cursor.execute('''SELECT id,user_id,username,role FROM user''').fetchall()
