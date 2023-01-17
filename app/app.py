import os
from flask import Flask, render_template, request, redirect, session, url_for
from auth import Auth
from data import Data

app = Flask(__name__)
app.secret_key = os.urandom(12)

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
    #@authenticate
    @Auth.check
    def index():
        user = session.get('user')
        content = 'index_content'
        return render_template('index.html', user = user, index_content = content)

    @app.route('/index_content')
    @Auth.check
    def index_content():
        D = Data()
        rows = D.get_nodes()
        for i in rows:
            print(i)
        return render_template('index_content.html', rows = rows)

    @app.route('/password', methods=['GET', 'POST'])
    @Auth.check
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
    @Auth.check
    def settings():
        user = session.get('user')
        return render_template('settings.html', user = user)

    @app.route('/users')
    @Auth.check
    def users():
        user = session.get('user')
        D = Data()
        users = D.users_select()
        return render_template('users.html', user = user, users = users)

    @app.route('/user_add', methods=['GET', 'POST'])
    @Auth.check
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
    @Auth.check
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
