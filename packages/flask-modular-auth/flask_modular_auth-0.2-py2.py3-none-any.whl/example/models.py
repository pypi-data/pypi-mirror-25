import datetime

from example.config import db, setup_auth
from flask_modular_auth import AbstractAuthEntity, current_authenticated_entity


class User(db.Model, AbstractAuthEntity):
    def get_roles(self):
        roles = ['user']
        if self.is_admin:
            roles.append('admin')
        return roles

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False, nullable=False)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    date = db.Column(db.DateTime(), default=datetime.datetime.now, nullable=False)
    title = db.Column(db.String(250), nullable=False)
    text = db.Column(db.Text(), nullable=False)

    @property
    def can_delete(self):
        if not current_authenticated_entity:
            return False
        elif current_authenticated_entity.is_admin:
            return True
        elif current_authenticated_entity == self.user:
            return True
        else:
            return False


def create_sample_data_on_first_start():
    count = db.session.query(db.func.count(User.id)).scalar()
    if count == 0:
        admin_user = User(username='admin', password='admin', is_admin=True)
        demo_user = User(username='demo', password='demo')
        db.session.add(admin_user)
        db.session.add(demo_user)
        post = BlogPost(user=admin_user, title='Welcome to the Simple Blog application.', text='This is the example application of the flask_modular_auth project. If you just started this up,'
                                                                                               'I have created two test users for you:'
                                                                                               '<ul>'
                                                                                               '<li>User "admin" with password "admin" is the blog administrator</li>'
                                                                                               '<li>User "demo" with password "demo" is a normal blog user'
                                                                                               '</ul>')
        db.session.add(post)
        db.session.commit()


def user_loader(**kwargs):
    if 'username' in kwargs and 'password' in kwargs:
        return User.query.filter_by(username=kwargs['username'], password=kwargs['password']).first()
    elif 'id' in kwargs:
        return User.query.filter_by(id=kwargs['id']).first()
    else:
        raise RuntimeError('This access method is not supported by the user loader.')


setup_auth(user_loader)
db.create_all()
