import sqlite3, os, hashlib
from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = os.urandom(12)

def authenticate(func):
    def wrapper(*args, **kwargs):
        if session.get('auth') is None:
            return redirect('/login')
        else: return func(*args, **kwargs)     
    wrapper.__name__ = func.__name__     
    return wrapper     

class Auth:
    def user_verify(self, user, password):
        D = Data()
        encrypt_password = hashlib.sha224(password.encode()).hexdigest()
        auth = D.user_auth(user, encrypt_password)
        if auth is None: return None
        else: return auth        

    def user_password_change(self, user, password):
        D = Data()
        encrypt_password = hashlib.sha224(password.encode()).hexdigest()
        D.user_password(user, encrypt_password)
        return True

    def user_initialize(self):
        #Check if admin user exists. If not create it
        D = Data()
        user = 'admin'
        password = 'password'
        encrypt_password = hashlib.sha224(password.encode()).hexdigest()
        D.user_create(user, encrypt_password)

    def user_add(self, user, password):
        D = Data()
        encrypt_password = hashlib.sha224(password.encode()).hexdigest()
        D.user_create(user, encrypt_password)

class Data:
    def __init__(self):
        self.con = sqlite3.connect('flask.db')
        self.cursor = self.con.cursor()

    def __del__(self):
        self.con.close()
    
    def create_tables(self):
        create_users = 'CREATE TABLE IF NOT EXISTS users (ID INTEGER PRIMARY KEY, user TEXT, password TEXT);'
        create_nodes = 'CREATE TABLE IF NOT EXISTS nodes (ID INTEGER PRIMARY KEY, name TEXT, ip TEXT, os TEXT);'
        create_metrics = 'CREATE TABLE IF NOT EXISTS metrics (ID INTEGER PRIMARY KEY, json JSON);'
        create_traces = 'CREATE TABLE IF NOT EXISTS traces (ID INTEGER PRIMARY KEY, json JSON);'
        create_logs = 'CREATE TABLE IF NOT EXISTS logs (ID INTEGER PRIMARY KEY, json JSON);'
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
        D.user_create(user, encrypt_password, role)
    

class Web:
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        if request.method == 'POST':
            user = request.form['user']
            password = request.form['password']
            A = Auth()
            auth = A.user_verify(user, password)
            if auth == user:
                session['user'] = user
                session['auth'] = True
                return redirect(url_for('index'))

    @app.route('/logoff')
    def logoff():
        session['auth'] = None
        session['user'] = None
        return redirect(url_for('login'))
        
    @app.route('/')
    @authenticate
    def index():
        user = session.get('user')
        content = 'index_content'
        return render_template('index.html', user = user, index_content = content)

    @app.route('/index_content')
    @authenticate
    def index_content():
        D = Data()
        rows = D.get_nodes()
        for i in rows:
            print(i)
        return render_template('index_content.html', rows = rows)

    @app.route('/password', methods=['GET', 'POST'])
    @authenticate
    def password():
        user = session.get('user')
        if request.method == 'GET':
            return render_template('password.html', user = user)
        if request.method == 'POST':
            password = request.form['password']
            A = Auth()
            A.user_password_change(user, password)
            return redirect(url_for('index'))
    
    @app.route('/settings')
    @authenticate
    def settings():
        user = session.get('user')
        return render_template('settings.html', user = user)

    @app.route('/users')
    @authenticate
    def users():
        user = session.get('user')
        D = Data()
        users = D.users_select()
        return render_template('users.html', user = user, users = users)

    @app.route('/user_add', methods=['GET', 'POST'])
    @authenticate
    def user_add():
        user = session.get('user')
        if request.method == 'GET':
            return render_template('user_add.html', user = user)
        if request.method == 'POST':
            user = request.form['user']
            password = request.form['password']
            A = Auth()
            A.user_add(user, password)
            return redirect(url_for('users'))

    @app.route('/user_pass/<user_edit>', methods=['GET', 'POST'])
    @authenticate
    def user_pass(user_edit):
        user = session.get('user')
        if request.method == 'GET':
            return render_template('user_pass.html', user = user, user_edit = user_edit)
        if request.method == 'POST':
            user_edit = request.form['user_edit']
            password = request.form['password']
            A = Auth()
            A.user_password_change(user_edit, password)
            return redirect(url_for('users'))


with app.app_context():
    D = Data()
    D.create_tables()
    D.load_data()
    A = Auth()
    A.user_initialize()

if __name__ == '__main__': 
    app.run()
