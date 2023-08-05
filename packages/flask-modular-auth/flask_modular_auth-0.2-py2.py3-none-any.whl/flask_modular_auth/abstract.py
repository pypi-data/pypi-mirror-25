class AbstractAuthProvider:
    def get_authenticated_entity(self):
        raise NotImplementedError('This method must be implemented in a subclass of AbstractAuthProvider!')


class AbstractAuthEntity:
    def get_roles(self):
        raise NotImplementedError('This method must be implemented in a subclass of AbstractAuthEntity!')

    @property
    def is_authenticated(self):
        raise NotImplementedError('This method must be implemented in a subclass of AbstractAuthEntity!')


class AbstractUnauthenticatedEntity(AbstractAuthEntity):
    def get_roles(self):
        return []

    @property
    def is_authenticated(self):
        return False


class AbstractPrivilege:
    def check(self):
        raise NotImplementedError('This method must be implemented in a subclass of AbstractPrivilege!')
