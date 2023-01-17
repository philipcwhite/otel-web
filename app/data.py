import hashlib, sqlite3

class Data:
    def __init__(self):
        self.con = sqlite3.connect('flask.db')
        self.cursor = self.con.cursor()

    def __del__(self):
        self.con.close()
    
    def create_tables(self):
        create_users = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user TEXT, password TEXT);'
        create_nodes = 'CREATE TABLE IF NOT EXISTS nodes (id INTEGER PRIMARY KEY, name TEXT, ip TEXT, os TEXT);'
        create_metrics = 'CREATE TABLE IF NOT EXISTS metrics (id INTEGER PRIMARY KEY, timestamp INTEGER, hostname TEXT, resource JSON, scopemetrics JSON);'
        create_traces = 'CREATE TABLE IF NOT EXISTS traces (id INTEGER PRIMARY KEY, timestamp INTEGER, hostname TEXT, resource JSON, scopespans JSON);'
        create_logs = 'CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, timestamp INTEGER, hostname TEXT, resource JSON, scopelogs JSON);'
        self.cursor.execute(create_users)
        self.cursor.execute(create_nodes)
        self.cursor.execute(create_metrics)
        self.cursor.execute(create_traces)
        self.cursor.execute(create_logs)
        self.con.commit()

    def load_data(self):
        insert_nodes = "INSERT INTO nodes VALUES (1, 'test01', '10.0.0.1', 'Linux'),(2, 'test02', '10.0.0.2', 'Windows') ON CONFLICT DO NOTHING;"
        self.cursor.execute(insert_nodes)
        self.con.commit()

    def get_nodes(self):
        sql = 'SELECT * FROM nodes;'
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def user_auth(self, user, encrypt_password):
        sql = "SELECT user from users where user=? AND password=?"
        self.cursor.execute(sql, (user, encrypt_password))
        result = self.cursor.fetchone()
        if not result is None:
            return result[0]   

    def user_password(self, user, password):
        sql = "UPDATE users SET password=? WHERE user=?"
        self.cursor.execute(sql, (password, user))
        self.con.commit()

    def users_select(self):
        sql = "SELECT id, user FROM users order by user" 
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        
    def user_select(self, id):
        sql = "SELECT id, user FROM users WHERE id=?" 
        self.cursor.execute(sql, (id))
        result = self.cursor.fetchone()
        return result
        
    def user_create(self, user, encrypt_pass):
        sql = "INSERT INTO users (user, password) SELECT ?, ? WHERE NOT EXISTS (SELECT * from users WHERE user=?) LIMIT 1"
        self.cursor.execute(sql, (user, encrypt_pass, user))
        self.con.commit()
        
    def user_delete(self, id):
        sql = "DELETE FROM users where id=?"
        self.cursor.execute(sql, (id))
        self.con.commit()

    def user_add(user, password):
        D = Data()
        encrypt_password = hashlib.sha224(password.encode()).hexdigest()
        D.user_create(user, encrypt_password)