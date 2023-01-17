import hashlib
from data import Data
from flask import redirect, session

class Auth:
    def check(func):
        def wrapper(*args, **kwargs):
            if session.get('auth') is None:
                return redirect('/login')
            else: return func(*args, **kwargs)     
        wrapper.__name__ = func.__name__     
        return wrapper  

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