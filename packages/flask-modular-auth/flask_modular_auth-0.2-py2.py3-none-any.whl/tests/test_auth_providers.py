import unittest
from base64 import b64encode
from flask import Flask
from flask_modular_auth import AuthManager, BasicAuthProvider, AbstractAuthEntity, AbstractUnauthenticatedEntity, current_authenticated_entity, privilege_required, RolePrivilege, KeyBasedAuthProvider, SessionBasedAuthProvider


class TestUserEntity(AbstractAuthEntity):
    @property
    def is_authenticated(self):
        return True

    def get_roles(self):
        return ['test']

    def get_id(self):
        return self.id

    def __init__(self, id, username):
        self.id = id
        self.username = username


def dummy_entity_loader(**kwargs):
    test_user_credentials = [
        (1, 'test_user', 'test_password', 'aeFiGh0mootoosohQueu')
    ]
    if 'username' in kwargs and 'password' in kwargs:
        for id, username, password, key in test_user_credentials:
            if username == kwargs['username'] and password == kwargs['password']:
                return TestUserEntity(id=id, username=username)
        return None
    elif 'key' in kwargs:
        for id, username, password, key in test_user_credentials:
            if key == kwargs['key']:
                return TestUserEntity(id=id, username=username)
        return None
    elif 'id' in kwargs:
        for id, username, password, key in test_user_credentials:
            if id == kwargs['id']:
                return TestUserEntity(id=id, username=username)
        return None
    else:
        raise RuntimeError('Unsupported entity loading method requested.')


class AuthProviderTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(AuthProviderTestCase, self).__init__(*args, **kwargs)
        self.app = Flask(__name__)
        self.app.secret_key = b'\xcd\xe1c\xfb\xccz7\xf6\xff\xe1\x8b\xf4\xb2\xd14\x93\xc1<\x8e\xd4\x16\xa7\x15z'
        self.manager = AuthManager(app=self.app)

        @self.app.route('/test')
        @privilege_required(RolePrivilege('test'))
        def test_view():
            return 'Hello World!'

        @self.app.route('/top_secret')
        @privilege_required(RolePrivilege('secret'))
        def top_secret_view():
            return 'Top secret!'


class BasicAuthProviderTestCase(AuthProviderTestCase):
    def __init__(self, *args, **kwargs):
        super(BasicAuthProviderTestCase, self).__init__(*args, **kwargs)
        self.manager.register_auth_provider(BasicAuthProvider(dummy_entity_loader))

    def test_authenticate_without_authorization_header(self):
        with self.app.test_request_context('/'):
            entity = current_authenticated_entity._get_current_object()
            self.assertIsInstance(entity, AbstractUnauthenticatedEntity)
            self.assertFalse(entity.is_authenticated)

    def test_authenticate_with_valid_data_returns_expected_entity(self):
        with self.app.test_request_context('/', headers={"Authorization": "Basic {}".format(b64encode(b'test_user:test_password').decode('ascii'))}):
            entity = current_authenticated_entity._get_current_object()
            self.assertIsInstance(entity, TestUserEntity)
            self.assertTrue(entity.is_authenticated)
            self.assertEqual(entity.username, 'test_user')

    def test_role_privilege_not_granted_for_secret_view(self):
        result = self.app.test_client().get('/top_secret', headers={"Authorization": "Basic {}".format(b64encode(b'test_user:test_password').decode('ascii'))})
        self.assertEqual(result.data, b'Not authorized')

    def test_role_privilege_granted_for_test_view(self):
        result = self.app.test_client().get('/test', headers={"Authorization": "Basic {}".format(b64encode(b'test_user:test_password').decode('ascii'))})
        self.assertEqual(result.data, b'Hello World!')

    def test_role_privilege_not_granted_for_test_view_without_authentication(self):
        result = self.app.test_client().get('/test')
        self.assertEqual(result.data, b'Not authorized')


class KeyBasedAuthProviderTestCase(AuthProviderTestCase):
    def __init__(self, *args, **kwargs):
        super(KeyBasedAuthProviderTestCase, self).__init__(*args, **kwargs)
        self.manager.register_auth_provider(KeyBasedAuthProvider(dummy_entity_loader))

    def test_authenticate_without_authorization_header(self):
        with self.app.test_request_context('/'):
            entity = current_authenticated_entity._get_current_object()
            self.assertIsInstance(entity, AbstractUnauthenticatedEntity)
            self.assertFalse(entity.is_authenticated)

    def test_authenticate_with_valid_data_returns_expected_entity(self):
        with self.app.test_request_context('/', headers={"Authorization": "APIKEY aeFiGh0mootoosohQueu"}):
            entity = current_authenticated_entity._get_current_object()
            self.assertIsInstance(entity, TestUserEntity)
            self.assertTrue(entity.is_authenticated)
            self.assertEqual(entity.username, 'test_user')

    def test_role_privilege_not_granted_for_secret_view(self):
        result = self.app.test_client().get('/top_secret', headers={"Authorization": "APIKEY aeFiGh0mootoosohQueu"})
        self.assertEqual(result.data, b'Not authorized')

    def test_role_privilege_granted_for_test_view(self):
        result = self.app.test_client().get('/test', headers={"Authorization": "APIKEY aeFiGh0mootoosohQueu"})
        self.assertEqual(result.data, b'Hello World!')

    def test_role_privilege_not_granted_for_test_view_without_authentication(self):
        result = self.app.test_client().get('/test')
        self.assertEqual(result.data, b'Not authorized')


class SessionBasedAuthProviderTestCase(AuthProviderTestCase):
    def __init__(self, *args, **kwargs):
        super(SessionBasedAuthProviderTestCase, self).__init__(*args, **kwargs)
        self.manager.register_auth_provider(SessionBasedAuthProvider(dummy_entity_loader))

        @self.app.route('/login')
        def login_view():
            user = dummy_entity_loader(id=1)
            self.manager.get_auth_providers()[0].login_entity(user)
            return 'Login successful!'

        @self.app.route('/logout')
        def logout_view():
            self.manager.get_auth_providers()[0].logout_entity()
            return 'Logout successful!'

    def test_authenticate_without_session(self):
        with self.app.test_request_context('/'):
            entity = current_authenticated_entity._get_current_object()
            self.assertIsInstance(entity, AbstractUnauthenticatedEntity)
            self.assertFalse(entity.is_authenticated)

    def test_restricted_page_not_accessible_before_login(self):
        c = self.app.test_client()
        result = c.get('/test')
        self.assertEqual(result.data, b'Not authorized')

    def test_restricted_page_accessible_after_login(self):
        c = self.app.test_client()
        c.get('/login')
        result = c.get('/test')
        self.assertEqual(result.data, b'Hello World!')

    def test_restricted_page_not_accessible_after_logout(self):
        c = self.app.test_client()
        c.get('/login')
        c.get('/logout')
        result = c.get('/test')
        self.assertEqual(result.data, b'Not authorized')

    def test_role_privilege_not_granted_for_secret_view(self):
        c = self.app.test_client()
        c.get('/login')
        result = c.get('/top_secret')
        self.assertEqual(result.data, b'Not authorized')


