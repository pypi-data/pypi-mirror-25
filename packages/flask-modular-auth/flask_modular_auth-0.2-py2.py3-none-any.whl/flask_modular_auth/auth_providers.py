import re
from flask import request, session
from .abstract import AbstractAuthProvider


class BasicAuthProvider(AbstractAuthProvider):
    """Authentication provider using HTTP basic auth

    This authentication provider supports *HTTP basic auth* to allow for authentication using a username and password.
    """
    def __init__(self, entity_loader):
        self._entity_loader = entity_loader

    def get_authenticated_entity(self):
        auth = request.authorization
        if not auth:
            return None
        else:
            return self._entity_loader(username=auth.username, password=auth.password)


class SessionBasedAuthProvider(AbstractAuthProvider):
    """Authentication provider using session cookies

    This authentication provider uses *session cookies* to store information about the authenticated entity. After a successful login, it uses the Flask session backend to store the ID of the logged in
    entity. Session data is removed when the entity is logged out.

    """
    def __init__(self, entity_loader, entity_cookie_name='authenticated_entity_id'):
        self._entity_loader = entity_loader
        self._entity_cookie_name = entity_cookie_name

    def get_authenticated_entity(self):
        if self._entity_cookie_name not in session:
            return None
        else:
            return self._entity_loader(id=session[self._entity_cookie_name])

    def login_entity(self, entity):
        """ This method should be called by your application once a client has succesfully logged in (e.g. by passing valid username and password credentials to a specific login view).

        :param entity: Should be an instance of :class:`AbstractAuthEntity`. Must provide ``id`` as an attribute or property, since this value will be saved to the session cookie for reference.
        """
        session[self._entity_cookie_name] = entity.get_id()

    def logout_entity(self):
        """ This method should be called when you want to terminate an active session (e.g. once a client accesses the logout view of your application). It does not need the currently authenticated
        entity as a parameter, since this is already determined by the active session.
        """
        session.pop(self._entity_cookie_name, None)


class KeyBasedAuthProvider(AbstractAuthProvider):
    """Authentication provider using special access keys

    This authentication provider uses a special key which is present in the HTTP Authorization header for authentication. This is commonly used in REST APIs and is also known as *API key
    authentication*. Instead of sending credentials such as a username and password with every request, each client is assigned an API key.
    """
    def __init__(self, entity_loader, header_key_name='APIKEY'):
        self._entity_loader = entity_loader
        self._header_key_name = header_key_name

    def get_authenticated_entity(self):
        if 'Authorization' not in request.headers:
            return None
        authorization_header = request.headers['Authorization']
        m = re.match('^{} (.*)$'.format(self._header_key_name), authorization_header)
        if not m:
            return None
        token = m.group(1)
        return self._entity_loader(key=token)
