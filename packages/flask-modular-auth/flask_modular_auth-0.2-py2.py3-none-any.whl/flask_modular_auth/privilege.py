from .utils import current_authenticated_entity
from .abstract import AbstractPrivilege


class AndPrivilege(AbstractPrivilege):
    def __init__(self, *privileges):
        self._privileges = privileges

    def check(self):
        for privilege in self._privileges:
            if not privilege.check():
                return False
        return True


class RolePrivilege(AbstractPrivilege):
    def __init__(self, role_name):
        self._role_name = role_name

    def check(self):
        return self._role_name in current_authenticated_entity.get_roles()


class AuthenticatedPrivilege(AbstractPrivilege):
    def check(self):
        return current_authenticated_entity.is_authenticated
