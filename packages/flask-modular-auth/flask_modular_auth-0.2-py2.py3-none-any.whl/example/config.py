from flask import Flask, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask.ext.modular_auth import AuthManager, SessionBasedAuthProvider, current_authenticated_entity


def unauthorized_callback():
    if current_authenticated_entity.is_authenticated:
        flash('You are not authorized to access this resource!', 'warning')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login', next=request.url))


def setup_auth(user_loader):
    app.session_provider = SessionBasedAuthProvider(user_loader)
    auth_manager.register_auth_provider(app.session_provider)


app = Flask(__name__)
db = SQLAlchemy(app)
auth_manager = AuthManager(app, unauthorized_callback=unauthorized_callback)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simple_blog.db'
app.config['SECRET_KEY'] = b'\xfaqh\x15\xf6\t\xcd\xb7\x11k\xd9m\xfb\xa3\x02Vp\xa7\x97\xed\xa2\x85$u'
Bootstrap(app)
