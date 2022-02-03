import unittest
from modela.server import Modela

class TestModela_dataproduct(unittest.TestCase):
    """Tests for `modela` package."""

    def setUp(self):
        self.modela = Modela("localhost", 3000)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        self.modela.close()

    def test_dataproduct_create(self):
        dataproduct = self.modela.DataProduct(namespace="default-tenant", name="test")
        assert dataproduct != None
        dataproduct.submit(password="test")

    def test_dataproduct_update(self):
        pass

    def test_dataproduct_get(self):
        dataproduct = self.modela.DataProduct(namespace="default-tenant", name="admin")
        print(dataproduct.metadata.labels)

    def test_dataproduct_delete(self):
        dataproduct = self.modela.DataProduct(namespace="default-tenant", name="test")
        dataproduct.delete()

    def test_dataproduct_list(self):
        print(len(self.modela.DataProduct.list("default-tenant")))




