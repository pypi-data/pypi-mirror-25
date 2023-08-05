import unittest
from flask import Flask
from flask_modular_auth import AuthManager


class ModularAuthTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ModularAuthTestCase, self).__init__(*args, **kwargs)
        self.app = Flask(__name__)
        AuthManager(self.app)
