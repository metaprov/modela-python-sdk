import unittest
from modela.server import Modela
from modela.Accounts import Account

class TestModela_account(unittest.TestCase):
    """Tests for `modela` package."""

    def setUp(self):
        self.modela = Modela("localhost", 3000)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        self.modela.close()

    def test_account_create(self):
        account = self.modela.Account(namespace="default-tenant", name="test")
        assert account != None
        account.submit(password="test")

    def test_account_update(self):
        pass

    def test_account_get(self):
        account = self.modela.Account(namespace="default-tenant", name="admin")
        print(account.metadata.labels)

    def test_account_delete(self):
        account = self.modela.Account(namespace="default-tenant", name="test")
        account.delete()

    def test_account_list(self):
        print(len(self.modela.Accounts.list("default-tenant")))



        
