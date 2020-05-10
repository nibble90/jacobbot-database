import sys, unittest
sys.path.append("../")

from database_security import AccessDatabase

class TestDatabaseSecurity(unittest.TestCase):
    def setUp(self):
        self.address = "192.168.0.0"
        self.AD = AccessDatabase(self.address)
    def test_reset(self):
        self.assertTrue(self.AD.reset_attempts())
    def test_add_attempt(self):
        self.assertTrue(self.AD.add_attempt())
    def test_attempts(self):
        self.assertEqual(self.AD.attempts(), 1)





if __name__ == "__main__":
    unittest.main()
