import sys, unittest
sys.path.append("../")

from database_access_layer import AccessDatabase

class TestDatabaseSecurity(unittest.TestCase):
    def setUp(self):
        self.AD = AccessDatabase()
        self.AD.ip_address = "192.168.0.0"
        self.AD.uuid = "123456"

    def test_reset(self):
        self.assertTrue(self.AD.reset_attempts())

    def test_add_attempt(self):
        self.assertTrue(self.AD.add_attempt())

    def test_attempts(self):
        self.assertEqual(self.AD.attempts(), 1)

    def test_add_user(self):
        if(self.AD.uuid_check()):
            self.assertTrue(self.AD.add_user())
        else:
            self.assertFalse(self.AD.add_user())

    def test_uuid_check(self):
        self.assertTrue(self.AD.uuid_check())

    def test_allow_access(self):
        attempts = int(self.AD.attempts())
        if(attempts >= 5):
            self.assertFalse(self.AD.check_access())
        else:
            self.assertTrue(self.AD.check_access())

    def test_blocked_true(self):
        for _ in range(self.AD.attempts(), 6):
            self.AD.add_attempt()
        self.AD.block_user()
        self.assertTrue(self.AD.check_block_status())

    def test_blocked_false(self):
        self.AD.unblock_user()
        self.assertFalse(self.AD.check_block_status())




if __name__ == "__main__":
    unittest.main()
