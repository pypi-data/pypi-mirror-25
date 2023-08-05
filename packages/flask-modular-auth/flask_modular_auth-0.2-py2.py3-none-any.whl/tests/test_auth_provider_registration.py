from flask_modular_auth import AbstractAuthProvider, current_authenticated_entity
from tests.modular_auth_test_case import ModularAuthTestCase


class AuthProvidersTestCase(ModularAuthTestCase):
    def test_get_auth_providers_initially_empty(self):
        self.assertEqual(self.app.auth_manager.get_auth_providers(), [])

    def test_cannot_register_abstract_auth_provider(self):
        with self.assertRaises(RuntimeError):
            self.app.auth_manager.register_auth_provider(AbstractAuthProvider())

    def test_cannot_register_other_object_as_auth_provider(self):
        class Something:
            pass
        with self.assertRaises(ValueError):
            self.app.auth_manager.register_auth_provider(Something())

    def test_get_authenticated_entity_raises_exception_without_auth_provider(self):
        with self.assertRaises(RuntimeError):
            with self.app.test_request_context('/'):
                str(current_authenticated_entity)
