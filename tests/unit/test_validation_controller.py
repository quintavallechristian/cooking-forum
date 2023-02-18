from website.controllers import ValidationController
import unittest
from faker import Faker

fake = Faker()


class TestClass(unittest.TestCase):
    def test_validate_correct_password(self):
        self.assertTrue(ValidationController.validatePassword("testPassword"))

    def test_validate_incorrect_password(self):
        self.assertFalse(ValidationController.validatePassword("test"))

    def test_validate_correct_email(self):
        self.assertTrue(ValidationController.validateEmail(fake.email()))

    def test_validate_incorrect_email(self):
        self.assertFalse(ValidationController.validateEmail("test"))

    def test_validate_correct_name(self):
        self.assertTrue(ValidationController.validateName(fake.name()))

    def test_validate_incorrect_name(self):
        self.assertFalse(ValidationController.validateName(""))

    def test_validate_correct2fa(self):
        self.assertTrue(ValidationController.validate2fa(True))

    def test_validate_incorrect_2fa(self):
        self.assertFalse(ValidationController.validate2fa(None))
