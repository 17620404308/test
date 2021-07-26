import unittest
from api.users import Users
class testAllUsers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = Users()

    @classmethod
    def tearDownClass(cls):
        pass

